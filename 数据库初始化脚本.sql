/* =========================================================
   MySQL 8.x  纯 SQL 脚本
   数据库：weChat_assistance
   建库 + 建表 + 授权（如已授权可删最后一段）
   直接复制到 Navicat → 新建查询 → 运行
   ========================================================= */

-- 1. 建库（如已存在先删除，生产环境请谨慎）
/* =========================================================
DROP DATABASE IF EXISTS weChat_assistance;
CREATE DATABASE weChat_assistance
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
   ========================================================= */

-- 2. 进入数据库
USE weChat_assistance;

-- 3. 客户端信息表
CREATE TABLE client_info (
    mac             VARCHAR(32)  NOT NULL COMMENT '客户端 MAC 地址',
    os_version      VARCHAR(64)  NOT NULL COMMENT '操作系统版本',
    client_name     VARCHAR(64)  NOT NULL COMMENT '客户端应用名',
    cpu_version     VARCHAR(64)  NOT NULL COMMENT 'CPU 型号',
    ip              VARCHAR(45)           COMMENT '内网/外网 IP',
    wechat_username VARCHAR(64)  NOT NULL COMMENT '登录的微信用户名',
    phone           VARCHAR(20)           COMMENT '手机号（可选）',
    login_time      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '首次上线时间',
    PRIMARY KEY (mac)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COMMENT='客户端基本信息';

-- 4. 授权信息表
CREATE TABLE lic_info (
    phone      VARCHAR(20) NOT NULL COMMENT '手机号',
    user_type  VARCHAR(32) NOT NULL COMMENT '过期 1个月 1年 永久',
    begin_time DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '授权开始时间',
    PRIMARY KEY (phone)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COMMENT='授权信息';


-- 5. 充值记录信息表
CREATE TABLE payment_info (
    phone        VARCHAR(20)    NOT NULL COMMENT '手机号',
    for_days     VARCHAR(4)      NOT NULL COMMENT '天数',
    payment_describe  VARCHAR(128)     NOT NULL COMMENT '充值描述',
    payment_time DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '充值时间',
    PRIMARY KEY (phone)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COMMENT='充值记录信息';

/* =========================================================
   运行完成后，在 Navicat 里刷新左侧列表即可看到
   weChat_assistance 库及其两张表。
   ========================================================= */