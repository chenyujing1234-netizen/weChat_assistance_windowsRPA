# -*- coding: utf-8 -*-
"""
通过本地微信数据库获取好友列表（微信4.x / Weixin.exe）

实现参考 E:\Source\WeChatDataAnalysis 工程：
- key_v4.py        : 从微信进程内存提取数据库密钥（V4）
- dll_key_scan.py  : 从 Weixin.dll 提取内部辅助key（新版微信的内存密钥被其异或掩码）
- wechat_decrypt.py: SQLCipher 4.0 格式的数据库解密
- chat_contacts.py : 联系人好友过滤规则

说明：
- AES/HMAC 依赖 pycryptodome（或旧版pycrypto，两者API兼容），
  PBKDF2 一律使用标准库 hashlib.pbkdf2_hmac（C实现，不受Crypto版本影响）。
  进程与内存操作通过 ctypes + psutil 完成，不依赖 pymem / yara-python / pefile。
- 对用户界面只表现为一个"初始化"过程；详细过程信息通过 log_fn 输出日志，
  日志中绝不输出密钥明文（仅输出数量/长度等统计信息）。
- Python 3.7 兼容语法。
"""

import os
import re
import sys
import time
import struct
import sqlite3
import ctypes
import hashlib
import tempfile
import traceback
from ctypes import wintypes

try:
    from Crypto.Cipher import AES as _AES
    from Crypto.Protocol.KDF import PBKDF2 as _PBKDF2
    from Crypto.Hash import SHA512 as _SHA512
    from Crypto.Hash import HMAC as _HMAC
    _HAS_PYCRYPTODOME = True
except Exception:
    _HAS_PYCRYPTODOME = False
    _AES = None
    _PBKDF2 = None
    _SHA512 = None
    _HMAC = None


def _crypto_env_desc():
    """当前进程实际加载的Crypto环境描述（用于诊断日志，不含敏感信息）"""
    try:
        import Crypto
        ver = getattr(Crypto, "__version__", "?")
        where = os.path.dirname(Crypto.__file__)
        return "Crypto {} ({})".format(ver, where)
    except Exception:
        return "Crypto不可用"


def _pbkdf2_sha512(password, salt, count, dklen=32):
    """PBKDF2-HMAC-SHA512。

    优先使用标准库 hashlib.pbkdf2_hmac（C实现，速度与Crypto无关，兼容性最好），
    失败时回退到 pycryptodome 的 PBKDF2。
    注意：不能用 pycrypto/旧版 pycryptodome 的 hmac_hash_module 关键字参数，
    旧版不支持该参数会抛 TypeError 且被上层静默吞掉，导致密钥校验全部失败。
    """
    try:
        return hashlib.pbkdf2_hmac("sha512", password, salt, count, dklen=dklen)
    except Exception:
        return _PBKDF2(password, salt, dkLen=dklen, count=count, hmac_hash_module=_SHA512)


####################################################################
# 密钥缓存（参考工程 key_store.py 思路）
# 数据库salt不变则密钥不变；成功提取一次后持久化，
# 此后即使微信重启/内存布局变化也能毫秒级完成校验。
# 缓存以 contact.db 的 salt 为索引，保存 enc_key 与（可推得时的）passphrase。
####################################################################

_KEY_CACHE_FILE = os.path.join(os.path.expanduser("~"), ".wechat_rpa_db_key_cache.json")


def _load_key_cache():
    import json
    try:
        with open(_KEY_CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


def _save_key_cache_entry(salt_hex, enc_key, passphrase, account_name):
    """salt_hex -> {"enc_key": hex, "passphrase": hex或空, "account": 名字}"""
    import json
    try:
        cache = _load_key_cache()
        cache[salt_hex] = {
            "enc_key": enc_key.hex(),
            "passphrase": passphrase.hex() if passphrase else "",
            "account": account_name,
        }
        tmp = _KEY_CACHE_FILE + ".tmp"
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(cache, f)
        os.replace(tmp, _KEY_CACHE_FILE)
    except Exception:
        pass  # 缓存写失败不影响主流程


def _try_cached_keys(account_db_list, log):
    """用缓存的密钥直接验证各账号数据库，命中返回
    (acc_name, db_path, enc_key, mac_key, passphrase) 或 None"""
    cache = _load_key_cache()
    if not cache:
        return None
    log("本地数据库初始化(5/5): 检查本地缓存的访问凭据... (共{}条)".format(len(cache)))
    for acc_name, db_path, _db_storage in account_db_list:
        try:
            with open(db_path, 'rb') as f:
                page1 = f.read(PAGE_SIZE)
        except OSError:
            continue
        if len(page1) < PAGE_SIZE or page1[:16] == SQLITE_HEADER:
            continue
        salt_hex = page1[:SALT_SIZE].hex()
        entry = cache.get(salt_hex)
        if not entry:
            continue
        # 优先enc_key直验(毫秒级)
        try:
            enc_key = bytes.fromhex(entry.get("enc_key", ""))
            r = _verify_key_material(enc_key, page1)
            if r is not None:
                log("本地数据库初始化(5/5): 缓存凭据验证成功(账号:{})".format(acc_name))
                return (acc_name, db_path, r[0], r[1], enc_key)
        except Exception:
            pass
        # 再试passphrase(含一次PBKDF2, 约0.25秒)
        try:
            passphrase = bytes.fromhex(entry.get("passphrase", ""))
            if passphrase:
                r = _verify_key_material(passphrase, page1)
                if r is not None:
                    log("本地数据库初始化(5/5): 缓存凭据验证成功(账号:{})".format(acc_name))
                    return (acc_name, db_path, r[0], r[1], passphrase)
        except Exception:
            pass
    return None

# SQLCipher 4.0 / WCDB 页面参数（与参考工程一致）
SQLITE_HEADER = b"SQLite format 3\x00"
PAGE_SIZE = 4096
SALT_SIZE = 16
IV_SIZE = 16
HMAC_SIZE = 64
RESERVE_SIZE = IV_SIZE + HMAC_SIZE  # 80
KEY_SIZE = 32
PBKDF2_ROUND_COUNT = 256000

# 内存中key指针结构的固定后缀特征（对应参考工程key_v4.py的yara规则）
# 完整特征: [6字节指针低位][00*10][20 00*7][2f 00*7]，匹配起点在6字节指针处
_KEY_PTR_SUFFIX = b"\x00" * 10 + b"\x20" + b"\x00" * 7 + b"\x2f" + b"\x00" * 7

# Windows API 常量
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400
MEM_COMMIT = 0x1000
MEM_PRIVATE = 0x20000
MAX_REGION_READ_SIZE = 1024 * 1024 * 1024  # 单个内存区域读取上限1GB

# 系统内置账号（不算好友），参考工程 _FRIEND_EXCLUDE_USERNAMES
_FRIEND_EXCLUDE_USERNAMES = {"medianote", "floatbottle", "qmessage", "qqmail", "fmessage"}

# Weixin.dll 内部辅助key特征（对应参考工程dll_key_scan.py）
_DLL_KEY_PATTERN = re.compile(
    b"\x48\xBA(.{8})"       # mov rdx, <8 bytes>
    b".{3,8}?"
    b"\x48\xBA(.{8})"
    b".{3,8}?"
    b"\x48\xBA(.{8})"
    b".{3,8}?"
    b"\x48\xBA(.{8})"
    b".{3,8}?"
    b"\x48\x85\xC0",       # test rax, rax
    re.DOTALL,
)
_DLL_CHUNK_SIZE = 2 * 1024 * 1024
_DLL_OVERLAP_SIZE = 100
_IMAGE_SCN_MEM_EXECUTE = 0x20000000


class WeChatDbError(Exception):
    """本地微信数据库操作异常（message可直接展示给用户）"""
    pass


def _default_log(msg):
    print(msg)


if os.name == 'nt':
    _kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    _kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _kernel32.OpenProcess.restype = wintypes.HANDLE
    _kernel32.ReadProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID,
                                            ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
    _kernel32.ReadProcessMemory.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.VirtualQueryEx.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID, ctypes.c_size_t]
    _kernel32.VirtualQueryEx.restype = ctypes.c_size_t
else:
    _kernel32 = None


class _MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", ctypes.c_ulong),
        ("RegionSize", ctypes.c_size_t),
        ("State", ctypes.c_ulong),
        ("Protect", ctypes.c_ulong),
        ("Type", ctypes.c_ulong),
    ]


####################################################################
# 微信进程
####################################################################

def find_wechat_processes():
    """返回 [[pid, name小写], ...]，Weixin.exe(4.x)优先排在前面"""
    import psutil
    out = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = str(proc.info.get('name') or '').lower()
            if name in ('weixin.exe', 'wechat.exe'):
                out.append([proc.info['pid'], name])
        except Exception:
            continue
    out.sort(key=lambda item: 0 if item[1] == 'weixin.exe' else 1)
    return out


def is_wechat_v4_running():
    """微信4.x(Weixin.exe)是否在运行"""
    for pid, name in find_wechat_processes():
        if name == 'weixin.exe':
            return True
    return False


def _get_process_exe_path(pid):
    try:
        import psutil
        return psutil.Process(int(pid)).exe()
    except Exception:
        return ""


####################################################################
# 微信数据目录定位
####################################################################

def _detect_data_roots():
    """自动查找微信4.x数据根目录(xwechat_files)，返回存在的目录列表"""
    roots = []

    def _add(path):
        try:
            if os.path.isdir(path) and path not in roots:
                roots.append(path)
        except Exception:
            pass

    # 默认位置: 文档\xwechat_files
    try:
        docs = os.path.join(os.path.expanduser("~"), "Documents")
        _add(os.path.join(docs, "xwechat_files"))
    except Exception:
        pass

    # 各盘符根目录下名称包含xwechat_files的目录（自定义保存位置）
    try:
        import string
        for ch in string.ascii_uppercase:
            drive_root = u"{}:\\".format(ch)
            if not os.path.isdir(drive_root):
                continue
            try:
                for name in os.listdir(drive_root):
                    if "xwechat_files" in name.lower():
                        _add(os.path.join(drive_root, name))
            except Exception:
                continue
    except Exception:
        pass

    return roots


def _account_name_variants(name):
    """账号目录名 wxid_xxx_abcd 可能带4位十六进制后缀，登录目录里是不带后缀的wxid_xxx"""
    out = {name}
    m = re.match(r"^(wxid_[^_\s]+)_[0-9a-fA-F]{4}$", name)
    if m:
        out.add(m.group(1))
    return out


def _detect_accounts(data_root):
    """枚举数据根目录下的账号目录（含db_storage），按最近活动时间降序返回
    返回 [[账号名, db_storage路径, 活动时间], ...]
    """
    accounts = []
    try:
        names = os.listdir(data_root)
    except Exception:
        return accounts

    login_dirs = []
    for sub in ("all_users/login", "login"):
        p = os.path.join(data_root, sub.replace("/", os.sep))
        if os.path.isdir(p):
            login_dirs.append(p)

    for name in names:
        if name.lower() in ("all_users", "backup", "tmp"):
            continue
        db_storage = os.path.join(data_root, name, "db_storage")
        if not os.path.isdir(db_storage):
            continue

        # 活动时间: 优先用登录目录下key_info.db的修改时间
        activity_time = 0
        for variant in _account_name_variants(name):
            for login_dir in login_dirs:
                key_info = os.path.join(login_dir, variant, "key_info.db")
                if os.path.isfile(key_info):
                    try:
                        activity_time = max(activity_time, os.path.getmtime(key_info))
                    except OSError:
                        pass
        # 兜底: db_storage目录的修改时间
        if activity_time == 0:
            try:
                activity_time = os.path.getmtime(db_storage)
            except OSError:
                activity_time = 0

        accounts.append([name, db_storage, activity_time])

    accounts.sort(key=lambda item: item[2], reverse=True)
    return accounts


def _find_contact_db(db_storage):
    """在db_storage下定位通讯录数据库，返回路径或None"""
    candidates = [
        os.path.join(db_storage, "contact", "contact.db"),
        os.path.join(db_storage, "contact.db"),
    ]
    for p in candidates:
        try:
            if os.path.isfile(p) and os.path.getsize(p) >= PAGE_SIZE:
                return p
        except OSError:
            continue
    return None


def _collect_probe_dbs(db_storage, contact_db, max_count=4):
    """收集用于密钥校验的探针数据库：contact.db 优先，再补充其他子目录的加密db。
    单个文件处于写入瞬态时，其他探针仍可完成校验。"""
    probes = []
    if contact_db:
        probes.append(contact_db)
    try:
        sub_names = sorted(os.listdir(db_storage))
    except OSError:
        return probes
    for sub in sub_names:
        if len(probes) >= max_count:
            break
        subdir = os.path.join(db_storage, sub)
        if not os.path.isdir(subdir):
            continue
        try:
            file_names = sorted(os.listdir(subdir))
        except OSError:
            continue
        for fname in file_names:
            if len(probes) >= max_count:
                break
            if not fname.endswith(".db"):
                continue
            p = os.path.join(subdir, fname)
            try:
                if os.path.isfile(p) and os.path.getsize(p) >= PAGE_SIZE and p not in probes:
                    probes.append(p)
            except OSError:
                continue
    return probes


####################################################################
# 进程内存密钥扫描（V4）
####################################################################

def _open_process_for_read(pid):
    if _kernel32 is None:
        raise WeChatDbError("仅支持Windows环境")
    handle = _kernel32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, int(pid))
    if not handle:
        raise WeChatDbError("无法访问微信进程内存（错误码{}），请尝试以管理员身份运行本程序".format(
            ctypes.get_last_error()))
    return handle


def _read_process_memory(handle, address, size):
    buf = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_size_t(0)
    ok = _kernel32.ReadProcessMemory(handle, ctypes.c_void_p(address), buf, size, ctypes.byref(bytes_read))
    if not ok:
        return None
    return buf.raw[:bytes_read.value]


def _enum_memory_regions(handle):
    """枚举 MEM_COMMIT + MEM_PRIVATE 内存区域，返回 [(base, size), ...]"""
    regions = []
    mbi = _MEMORY_BASIC_INFORMATION()
    address = 0
    while True:
        ret = _kernel32.VirtualQueryEx(handle, ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi))
        if not ret:
            break
        if mbi.State == MEM_COMMIT and mbi.Type == MEM_PRIVATE:
            base = mbi.BaseAddress if mbi.BaseAddress is not None else 0
            if base and mbi.RegionSize and mbi.RegionSize <= MAX_REGION_READ_SIZE:
                regions.append((base, mbi.RegionSize))
        if mbi.RegionSize == 0:
            break
        address += mbi.RegionSize
        if address > 0x7FFFFFFFFFFF:
            break
    return regions


def _is_potential_key(key):
    """熵过滤：32字节、相异字节>=15、可打印字符<=24（参考工程key_v4.py）"""
    if not key or len(key) != KEY_SIZE:
        return False
    if len(set(key)) < 15:
        return False
    printable_count = sum(1 for b in key if 32 <= b <= 126)
    if printable_count > 24:
        return False
    return True


def _scan_memory_key_candidates(pid, log_fn):
    """扫描微信进程内存，返回熵过滤后的候选raw key列表（bytes）"""
    handle = _open_process_for_read(pid)
    try:
        regions = _enum_memory_regions(handle)
        log_fn("本地数据库初始化: 内存区域数量{}".format(len(regions)))
        ptr_list = []
        total_bytes = 0
        for base, size in regions:
            data = _read_process_memory(handle, base, size)
            if not data:
                continue
            total_bytes += len(data)
            pos = 0
            while True:
                idx = data.find(_KEY_PTR_SUFFIX, pos)
                if idx < 0:
                    break
                if idx >= 6:
                    try:
                        ptr = struct.unpack_from('<Q', data, idx - 6)[0]
                    except struct.error:
                        ptr = 0
                    # 合法用户态指针
                    if 0x10000 <= ptr < 0x7FFFFFFFFFFF:
                        ptr_list.append(ptr)
                pos = idx + 1

        log_fn("本地数据库初始化: 内存扫描完成, 共扫描{:.1f}MB, 命中指针特征{}个".format(
            total_bytes / 1024.0 / 1024.0, len(ptr_list)))

        # 指针去重后读取32字节候选key
        keys = []
        seen = set()
        for ptr in ptr_list:
            if ptr in seen:
                continue
            seen.add(ptr)
            key_bytes = _read_process_memory(handle, ptr, KEY_SIZE)
            if not key_bytes or len(key_bytes) != KEY_SIZE:
                continue
            if key_bytes in seen:
                continue
            seen.add(key_bytes)
            keys.append(key_bytes)

        filtered = [k for k in keys if _is_potential_key(k)]
        log_fn("本地数据库初始化: 候选数据提取完成, 原始{}个, 过滤后{}个".format(len(keys), len(filtered)))
        return filtered
    finally:
        try:
            _kernel32.CloseHandle(handle)
        except Exception:
            pass


####################################################################
# Weixin.dll 内部辅助key扫描
####################################################################

def _pe_code_sections(dll_path):
    """手工解析PE文件，返回代码段的 [(文件偏移, 原始大小, 虚拟地址), ...]"""
    sections = []
    with open(dll_path, 'rb') as f:
        head = f.read(0x400)
        if len(head) < 0x40 or head[:2] != b'MZ':
            return sections
        e_lfanew = struct.unpack_from('<I', head, 0x3C)[0]
        if e_lfanew <= 0:
            return sections
        f.seek(e_lfanew)
        pe_head = f.read(4 + 20 + 8)
        if len(pe_head) < 4 + 20 or pe_head[:4] != b'PE\x00\x00':
            return sections
        n_sections = struct.unpack_from('<H', pe_head, 4 + 2)[0]
        opt_size = struct.unpack_from('<H', pe_head, 4 + 16)[0]
        opt_off = 4 + 20
        f.seek(e_lfanew + opt_off)
        opt_head = f.read(max(opt_size, 32))
        if len(opt_head) < 32:
            return sections
        magic = struct.unpack_from('<H', opt_head, 0)[0]
        if magic == 0x20B:  # PE32+
            image_base = struct.unpack_from('<Q', opt_head, 24)[0]
        else:  # PE32
            image_base = struct.unpack_from('<I', opt_head, 28)[0]

        sec_table_off = e_lfanew + opt_off + opt_size
        f.seek(sec_table_off)
        raw = f.read(40 * n_sections)
        if len(raw) < 40 * n_sections:
            return sections

        for i in range(n_sections):
            off = i * 40
            vsize, vaddr, rsize, rptr = struct.unpack_from('<IIII', raw, off + 8)
            characteristics = struct.unpack_from('<I', raw, off + 36)[0]
            if (characteristics & _IMAGE_SCN_MEM_EXECUTE) and rsize > 0:
                sections.append((rptr, rsize, image_base + vaddr))
    return sections


def _find_weixin_dll_candidates(exe_path):
    """根据微信进程可执行文件路径查找Weixin.dll候选，按修改时间降序"""
    candidates = []
    exe_dir = os.path.dirname(exe_path)
    direct = os.path.join(exe_dir, "Weixin.dll")
    if os.path.isfile(direct):
        candidates.append(direct)
    try:
        for name in os.listdir(exe_dir):
            sub = os.path.join(exe_dir, name)
            if not os.path.isdir(sub):
                continue
            c = os.path.join(sub, "Weixin.dll")
            if os.path.isfile(c):
                candidates.append(c)
            install_dir = os.path.join(sub, "install")
            if os.path.isdir(install_dir):
                for name2 in os.listdir(install_dir):
                    c2 = os.path.join(install_dir, name2, "Weixin.dll")
                    if os.path.isfile(c2):
                        candidates.append(c2)
    except OSError:
        pass

    dedup = []
    for c in candidates:
        if c not in dedup:
            dedup.append(c)
    try:
        dedup.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    except OSError:
        pass
    return dedup


def _scan_dll_internal_keys(dll_path, log_fn):
    """扫描Weixin.dll提取内部辅助key候选（32字节bytes列表）"""
    try:
        sections = _pe_code_sections(dll_path)
    except Exception as e:
        log_fn("本地数据库初始化: DLL解析失败({})".format(e))
        return []
    if not sections:
        log_fn("本地数据库初始化: DLL中未找到代码段")
        return []

    keys = []
    seen = set()
    with open(dll_path, 'rb') as f:
        for file_offset, size, base_va in sections:
            chunk_start = 0
            while chunk_start < size:
                chunk_size = min(_DLL_CHUNK_SIZE, size - chunk_start)
                f.seek(file_offset + chunk_start)
                chunk = f.read(chunk_size + _DLL_OVERLAP_SIZE)
                if not chunk:
                    break
                offset = 0
                while True:
                    idx = chunk.find(b"\x48\xBA", offset)
                    if idx == -1 or idx >= chunk_size:
                        break
                    m = _DLL_KEY_PATTERN.match(chunk[idx: idx + 85])
                    if m:
                        key_bytes = m.group(1) + m.group(2) + m.group(3) + m.group(4)
                        if key_bytes not in seen:
                            seen.add(key_bytes)
                            keys.append(key_bytes)
                        offset = idx + len(m.group(0))
                    else:
                        offset = idx + 1
                chunk_start += chunk_size

    log_fn("本地数据库初始化: 辅助数据扫描完成, 命中{}个".format(len(keys)))
    return keys


####################################################################
# 密钥验证与数据库解密（SQLCipher 4.0）
####################################################################

def _xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def _derive_mac_key(enc_key, salt):
    mac_salt = _xor_bytes(salt, b"\x3a" * SALT_SIZE)
    return _pbkdf2_sha512(enc_key, mac_salt, 2, KEY_SIZE)


def _compute_page_hmac(mac_key, page, page_num):
    offset = SALT_SIZE if page_num == 1 else 0
    data_end = PAGE_SIZE - RESERVE_SIZE + IV_SIZE  # 4032: 数据+IV参与HMAC
    h = _HMAC.new(mac_key, digestmod=_SHA512)
    h.update(page[offset:data_end])
    h.update(struct.pack('<I', page_num))
    return h.digest()


def _verify_key_material(key_material, page1):
    """验证候选密钥是否匹配数据库第1页。
    返回 (enc_key, mac_key) 或 None。key_material可能是passphrase也可能是raw enc_key。
    """
    if len(page1) < PAGE_SIZE:
        return None
    salt = page1[:SALT_SIZE]
    stored_hmac = page1[PAGE_SIZE - HMAC_SIZE: PAGE_SIZE]

    candidates = []
    # 模式1: key_material直接就是enc_key
    try:
        candidates.append(key_material)
    except Exception:
        pass
    # 模式2: key_material是passphrase, 需PBKDF2派生
    try:
        derived = _pbkdf2_sha512(key_material, salt, PBKDF2_ROUND_COUNT, KEY_SIZE)
        candidates.append(derived)
    except Exception:
        pass

    import hmac as _hmac_std
    for enc_key in candidates:
        try:
            mac_key = _derive_mac_key(enc_key, salt)
            expected = _compute_page_hmac(mac_key, page1, 1)
            if _hmac_std.compare_digest(expected, stored_hmac):
                return enc_key, mac_key
        except Exception:
            continue
    return None


def _brute_force_enc_key_scan(weixin_procs, db_path, log):
    """全内存暴力兜底：不依赖指针特征，对全部MEM_PRIVATE内存按4字节步长
    扫描高熵32字节窗口，直接以enc_key模式验证(每次仅2轮PBKDF2+一次HMAC, 微秒级)。
    适用于新版微信内存结构变化导致指针特征扫描失效的场景。
    返回 (enc_key, mac_key) 或 None。"""
    import hmac as _hmac_std
    try:
        with open(db_path, 'rb') as f:
            page1 = f.read(PAGE_SIZE)
    except OSError:
        return None
    if len(page1) < PAGE_SIZE or page1[:16] == SQLITE_HEADER:
        return None
    salt = page1[:SALT_SIZE]
    stored_hmac = page1[PAGE_SIZE - HMAC_SIZE: PAGE_SIZE]
    mac_salt = _xor_bytes(salt, b"\x3a" * SALT_SIZE)
    page_body = page1[SALT_SIZE: PAGE_SIZE - RESERVE_SIZE + IV_SIZE]
    pn1 = struct.pack('<I', 1)

    t0 = time.time()
    scanned_mb = 0.0
    tested = 0
    log("本地数据库初始化(5/5): 常规校验未匹配, 启用深度数据扫描(可能需要1-3分钟, 请稍候)...")
    for pid, _name in weixin_procs:
        try:
            handle = _open_process_for_read(pid)
        except WeChatDbError as e:
            log("本地数据库初始化(5/5): PID:{} 无法访问({})".format(pid, e))
            continue
        try:
            regions = _enum_memory_regions(handle)
            for base, size in regions:
                data = _read_process_memory(handle, base, size)
                if not data or len(data) < 64:
                    continue
                scanned_mb += len(data) / 1048576.0
                n = len(data)
                for off in range(0, n - 32, 4):
                    win = data[off:off + 32]
                    # 熵筛: 与_is_potential_key一致(distinct>=15)
                    if len(set(win)) < 15:
                        continue
                    tested += 1
                    mac_key = _pbkdf2_sha512(win, mac_salt, 2, KEY_SIZE)
                    m = _hmac_std.new(mac_key, page_body + pn1, hashlib.sha512)
                    if m.digest() == stored_hmac:
                        log("本地数据库初始化(5/5): 深度扫描命中 (耗时{:.0f}秒, 校验{}个特征)".format(
                            time.time() - t0, tested))
                        return win, mac_key
        finally:
            try:
                _kernel32.CloseHandle(handle)
            except Exception:
                pass
        log("本地数据库初始化(5/5): 深度扫描进度: 已扫描{:.0f}MB (PID:{})".format(scanned_mb, pid))
    log("本地数据库初始化(5/5): 深度扫描完成未命中 (扫描{:.0f}MB, 校验{}个特征, 耗时{:.0f}秒)".format(
        scanned_mb, tested, time.time() - t0))
    return None


def _decrypt_page(enc_key, page, page_num):
    """解密单个4096字节页面，输出明文SQLite页（保留80字节0填充）"""
    iv = page[PAGE_SIZE - RESERVE_SIZE: PAGE_SIZE - RESERVE_SIZE + IV_SIZE]
    offset = SALT_SIZE if page_num == 1 else 0
    encrypted = page[offset: PAGE_SIZE - RESERVE_SIZE]
    cipher = _AES.new(enc_key, _AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    if page_num == 1:
        return SQLITE_HEADER + decrypted + (b"\x00" * RESERVE_SIZE)
    return decrypted + (b"\x00" * RESERVE_SIZE)


def decrypt_database_file(db_path, enc_key, mac_key, log_fn):
    """解密整个数据库文件，返回明文SQLite数据(bytes)"""
    with open(db_path, 'rb') as f:
        data = f.read()
    if len(data) < PAGE_SIZE:
        raise WeChatDbError("数据库文件太小: {}".format(os.path.basename(db_path)))

    total_pages = (len(data) + PAGE_SIZE - 1) // PAGE_SIZE
    out = bytearray()
    import hmac as _hmac_std
    failed_pages = 0
    for cur in range(total_pages):
        page_num = cur + 1
        page = data[cur * PAGE_SIZE: (cur + 1) * PAGE_SIZE]
        if len(page) < PAGE_SIZE:
            page = page + (b"\x00" * (PAGE_SIZE - len(page)))
        # HMAC校验失败仅告警，仍尝试解密（参考工程策略）
        try:
            stored = page[PAGE_SIZE - HMAC_SIZE: PAGE_SIZE]
            expected = _compute_page_hmac(mac_key, page, page_num)
            if not _hmac_std.compare_digest(stored, expected):
                pass  # 页面HMAC不匹配（如1GiB边界页），保留解密
        except Exception:
            pass
        try:
            out.extend(_decrypt_page(enc_key, page, page_num))
        except Exception:
            failed_pages += 1
            out.extend(b"\x00" * PAGE_SIZE)

    if failed_pages > 0:
        log_fn("本地数据库初始化: 解密完成, 共{}页, 失败{}页(已用空页占位)".format(total_pages, failed_pages))
    else:
        log_fn("本地数据库初始化: 解密完成, 共{}页".format(total_pages))
    return bytes(out)


####################################################################
# 好友查询
####################################################################

def _pick_row_value(row, *names):
    """大小写不敏感地从sqlite行里取列值"""
    lower_map = {}
    for k in row.keys():
        lower_map[k.lower()] = k
    for name in names:
        col = lower_map.get(name.lower())
        if col is not None:
            v = row[col]
            if v is not None:
                return v
    return None


def _to_int(v):
    try:
        return int(v)
    except Exception:
        return 0


def _to_str(v):
    try:
        if v is None:
            return ""
        if isinstance(v, bytes):
            return v.decode("utf-8", errors="ignore")
        return str(v)
    except Exception:
        return ""


def _is_friend_row(username, local_type, flag, verify_flag):
    """判断contact表中的一行是否是真正的好友（参考chat_contacts.py规则，有简化）"""
    if not username:
        return False
    u = username.lower()
    if username.endswith("@chatroom"):
        return False            # 群聊
    if u == "weixin" or username.startswith("gh_"):
        return False            # 公众号/系统账号
    if u.startswith("weixin"):
        return False            # 微信团队等系统账号(weixin_team等)
    if u in _FRIEND_EXCLUDE_USERNAMES:
        return False            # 系统功能账号
    if (flag & 8) == 8:
        return False            # 已拉黑
    if local_type == 4 and verify_flag != 0:
        return False            # 认证的公众号
    return local_type == 1


def query_friends_from_plain_db(plain_db_path, log_fn):
    """在解密后的通讯录数据库中查询好友，返回好友信息dict列表"""
    conn = None
    try:
        conn = sqlite3.connect(plain_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [str(r[0]) for r in cursor.fetchall()]
        contact_table = None
        for t in table_names:
            if t.lower() == "contact":
                contact_table = t
                break
        if contact_table is None:
            raise WeChatDbError("通讯录数据库中未找到contact表")

        rows = conn.execute("SELECT * FROM {}".format(contact_table)).fetchall()
        friend_list = []
        skipped = 0
        for row in rows:
            username = _to_str(_pick_row_value(row, "username", "user_name"))
            local_type = _to_int(_pick_row_value(row, "local_type", "localType", "WCDB_CT_local_type"))
            flag = _to_int(_pick_row_value(row, "flag", "contact_flag", "contactFlag", "WCDB_CT_flag"))
            verify_flag = _to_int(_pick_row_value(row, "verify_flag", "verifyFlag", "VerifyFlag"))
            if not _is_friend_row(username, local_type, flag, verify_flag):
                skipped += 1
                continue
            nick_name = _to_str(_pick_row_value(row, "nick_name", "nickname", "nickName", "NickName",
                                                "WCDB_CT_nick_name"))
            remark = _to_str(_pick_row_value(row, "remark", "Remark", "WCDB_CT_remark"))
            # 展示名与RPA通讯录视图一致: 优先备注, 其次昵称
            display_name = remark if remark else (nick_name if nick_name else username)
            friend_list.append({
                "username": username,
                "friend_name": display_name,
                "nick_name": nick_name,
                "remark": remark,
                "alias": _to_str(_pick_row_value(row, "alias", "Alias", "WCDB_CT_alias")),
            })
        log_fn("本地数据库初始化: 解析通讯录完成, 联系人总数{}, 好友{}个(已排除群聊/公众号/系统账号{})".format(
            len(rows), len(friend_list), skipped))
        return friend_list
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


####################################################################
# 主流程
####################################################################

def sync_friends_from_local_db(log_fn=None):
    """通过本地微信数据库同步好友列表。

    返回 (iRet, friend_list, err_msg):
      iRet: 0成功; 非0失败
      friend_list: 成功时返回 [{"friend_name","add_date","friend_remark","username",...}, ...]
      err_msg: 失败原因（可直接展示）
    """
    log = log_fn if log_fn is not None else _default_log
    t_begin = time.time()

    if os.name != 'nt':
        return -1, [], "本地数据库方式仅支持Windows环境"
    if not _HAS_PYCRYPTODOME:
        return -1, [], "缺少加密组件(pycryptodome)，无法使用本地数据库方式"

    try:
        # ---------------- 步骤1: 微信进程 ----------------
        log("本地数据库初始化(1/5): 检测微信进程...")
        procs = find_wechat_processes()
        weixin_procs = [p for p in procs if p[1] == 'weixin.exe']
        if not weixin_procs:
            if procs:
                return -1, [], "检测到的是旧版微信(WeChat.exe)，本地数据库方式仅支持微信4.x(Weixin)，请升级微信后重试，或使用【同步好友】方式"
            return -1, [], "未检测到运行中的微信。本地数据库方式要求微信(4.x)处于登录状态，请先打开微信并登录后再试"
        log("本地数据库初始化(1/5): 检测到微信进程 Weixin.exe (PID:{})".format(weixin_procs[0][0]))

        # ---------------- 步骤2: 数据目录 ----------------
        log("本地数据库初始化(2/5): 定位本地数据目录...")
        data_roots = _detect_data_roots()
        accounts = []
        used_root = None
        for root in data_roots:
            accs = _detect_accounts(root)
            if accs:
                accounts = accs
                used_root = root
                break
        if not accounts:
            return -1, [], "未找到微信本地数据目录(默认在 文档\\xwechat_files)。请确认微信已在此电脑上登录过，且数据目录未被自定义移动"
        acc_names = ", ".join([a[0] for a in accounts[:3]])
        log("本地数据库初始化(2/5): 数据目录定位成功, 账号数据目录: {} (按最近活动优先尝试)".format(acc_names))

        # 为每个账号定位通讯录数据库
        account_db_list = []  # [[账号名, contact_db路径, db_storage路径], ...]
        for name, db_storage, _t in accounts:
            contact_db = _find_contact_db(db_storage)
            if contact_db:
                account_db_list.append([name, contact_db, db_storage])
        if not account_db_list:
            return -1, [], "数据目录中未找到通讯录数据库(contact.db)。请确认微信已完整登录"

        # ---------------- 步骤3: 内存密钥候选 ----------------
        log("本地数据库初始化(3/5): 扫描进程数据特征...")
        raw_keys = []
        seen = set()
        for pid, _name in weixin_procs:
            try:
                keys = _scan_memory_key_candidates(pid, log)
                for k in keys:
                    if k not in seen:
                        seen.add(k)
                        raw_keys.append(k)
            except WeChatDbError as e:
                log("本地数据库初始化(3/5): PID:{} 扫描失败({})".format(pid, e))
        if not raw_keys:
            return -1, [], "未能从微信进程中提取到有效的数据特征。请确保微信已登录且为4.x版本(Weixin)"
        log("本地数据库初始化(3/5): 特征数据合并完成, 共{}个候选".format(len(raw_keys)))

        # ---------------- 步骤4: 辅助key(DLL) ----------------
        log("本地数据库初始化(4/5): 分析程序辅助数据...")
        dll_keys = []
        exe_path = _get_process_exe_path(weixin_procs[0][0])
        if exe_path:
            dll_candidates = _find_weixin_dll_candidates(exe_path)
            for dll_path in dll_candidates:
                try:
                    dll_keys = _scan_dll_internal_keys(dll_path, log)
                except Exception as e:
                    log("本地数据库初始化(4/5): DLL分析异常({})".format(e))
                if dll_keys:
                    break
        else:
            log("本地数据库初始化(4/5): 无法获取微信安装路径, 跳过辅助数据分析")

        # ---------------- 步骤5: 验证并解密 ----------------
        log("本地数据库初始化(5/5): 校验数据环境...")
        log("本地数据库初始化(5/5): 运行环境: python={}, {}".format(sys.executable, _crypto_env_desc()))

        def _build_candidates(raw_list, dll_list):
            # 候选passphrase: 优先 raw XOR dll_key（新版微信），兜底 raw（旧版4.0）
            cands = []
            for dk in dll_list:
                for rk in raw_list:
                    cands.append(_xor_bytes(rk, dk))
            for rk in raw_list:
                cands.append(rk)
            uniq = []
            uniq_seen = set()
            for c in cands:
                if c not in uniq_seen:
                    uniq_seen.add(c)
                    uniq.append(c)
            return uniq

        def _run_verify(cands):
            """对每个账号依次用多个探针数据库校验候选密钥，返回 verified 或 None"""
            verified_local = None
            for acc_name, db_path, db_storage in account_db_list:
                if verified_local is not None:
                    break
                probe_list = _collect_probe_dbs(db_storage, db_path)
                for probe_path in probe_list:
                    if verified_local is not None:
                        break
                    try:
                        with open(probe_path, 'rb') as f:
                            page1 = f.read(PAGE_SIZE)
                    except OSError:
                        continue
                    if len(page1) < PAGE_SIZE:
                        continue
                    if page1[:16] == SQLITE_HEADER:
                        # 未加密数据库：只有通讯录库本身未加密时才直接采用
                        if probe_path == db_path:
                            verified_local = (acc_name, db_path, None, None, None)
                            log("本地数据库初始化(5/5): 数据库为未加密格式, 直接读取")
                        continue
                    log("本地数据库初始化(5/5): 校验数据文件[{}]...".format(os.path.basename(probe_path)))
                    for _ci, cand in enumerate(cands):
                        if _ci > 0 and _ci % 20 == 0:
                            log("本地数据库初始化(5/5): 校验进行中... {}/{}".format(_ci, len(cands)))
                        r = _verify_key_material(cand, page1)
                        if r is not None:
                            # cand==enc_key为直验模式; 否则cand是passphrase
                            passphrase = cand if cand != r[0] else None
                            verified_local = (acc_name, db_path, r[0], r[1], passphrase)
                            break
                if verified_local is None:
                    log("本地数据库初始化(5/5): 账号[{}]数据环境不匹配, 尝试下一个账号数据目录".format(acc_name))
            return verified_local

        # 5a. 缓存凭据优先(毫秒级)
        verified = _try_cached_keys(account_db_list, log)

        # 5b. 内存指针特征扫描验证
        if verified is None:
            passphrase_candidates = _build_candidates(raw_keys, dll_keys)
            verified = _run_verify(passphrase_candidates)
        else:
            passphrase_candidates = []

        # 5c. 全内存深度扫描兜底(新版微信内存结构变化时指针特征可能失效)
        if verified is None:
            acc0, db0, _s0 = account_db_list[0]
            bf = _brute_force_enc_key_scan(weixin_procs, db0, log)
            if bf is not None:
                verified = (acc0, db0, bf[0], bf[1], None)

        # 5d. 首轮未匹配: 可能微信刚完成登录或处于数据写入瞬态, 等待后重扫进程特征再试一轮
        if verified is None:
            log("本地数据库初始化(5/5): 首轮校验未匹配, 重新扫描进程数据特征后重试...")
            time.sleep(2)
            for pid, _name in weixin_procs:
                try:
                    keys = _scan_memory_key_candidates(pid, log)
                    for k in keys:
                        if k not in seen:
                            seen.add(k)
                            raw_keys.append(k)
                except WeChatDbError as e:
                    log("本地数据库初始化(5/5): PID:{} 扫描失败({})".format(pid, e))
            passphrase_candidates = _build_candidates(raw_keys, dll_keys)
            verified = _run_verify(passphrase_candidates)

        if verified is None:
            log("!!!!本地数据库初始化诊断: 特征候选{}个, 辅助key{}个, 校验组合{}个, 均未匹配; 运行环境: python={}, {}".format(
                len(raw_keys), len(dll_keys), len(passphrase_candidates) if passphrase_candidates else 0,
                sys.executable, _crypto_env_desc()))
            return -1, [], "数据环境校验失败：未能与本地数据库建立有效匹配。请确保微信已登录本机且数据目录完整，然后重试；或改用【同步好友】方式"

        acc_name, db_path, enc_key, mac_key, hit_passphrase = verified
        log("本地数据库初始化(5/5): 数据环境校验成功 (账号:{}, 耗时{:.1f}秒)".format(acc_name, time.time() - t_begin))

        # 校验成功后持久化密钥缓存: 数据库salt不变期间下次可毫秒级完成
        if enc_key is not None:
            try:
                with open(db_path, 'rb') as f:
                    salt_hex = f.read(SALT_SIZE).hex()
                _save_key_cache_entry(salt_hex, enc_key, hit_passphrase, acc_name)
                log("本地数据库初始化(5/5): 访问凭据已缓存, 后续同步将更快")
            except Exception:
                pass
        log("本地数据库初始化完成, 开始读取通讯录...")

        # ---------------- 步骤6: 解密 + 查询好友 ----------------
        tmp_path = None
        try:
            if enc_key is None:
                # 未加密数据库: 直接复制查询
                with open(db_path, 'rb') as f:
                    plain_data = f.read()
            else:
                plain_data = decrypt_database_file(db_path, enc_key, mac_key, log)

            fd, tmp_path = tempfile.mkstemp(prefix="wchat_contact_", suffix=".db")
            with os.fdopen(fd, 'wb') as f:
                f.write(plain_data)

            friends = query_friends_from_plain_db(tmp_path, log)
        finally:
            if tmp_path:
                for suffix in ("", "-wal", "-shm", "-journal"):
                    try:
                        os.unlink(tmp_path + suffix)
                    except OSError:
                        pass

        # 转成与RPA同步一致的FRIEND_INFO_LIST结构
        friend_info_list = []
        for f in friends:
            friend_info_list.append({
                "friend_name": f["friend_name"],
                "add_date": "",
                "friend_remark": "",
            })
        log("^-^本地数据库方式同步通讯录成功, 共{}个好友, 总耗时{:.1f}秒".format(
            len(friend_info_list), time.time() - t_begin))
        return 0, friend_info_list, ""

    except WeChatDbError as e:
        return -1, [], str(e)
    except Exception as e:
        log("!!!!本地数据库方式异常: {}".format(e))
        traceback.print_exc()
        return -1, [], "本地数据库方式发生异常: {}".format(e)


####################################################################
# 独立测试入口: python wechat_db_helper.py
####################################################################
if __name__ == '__main__':
    def _test_log(msg):
        print("[TEST] {}".format(msg))

    i_ret, friend_list, err = sync_friends_from_local_db(_test_log)
    if i_ret != 0:
        print("FAILED: {}".format(err))
    else:
        print("SUCCESS: {} friends".format(len(friend_list)))
        for f in friend_list[:10]:
            print("  - {}".format(f["friend_name"]))
