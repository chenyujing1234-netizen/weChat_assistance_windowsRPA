/*
 Navicat Premium Data Transfer

 Source Server         : 114.55.254.123
 Source Server Type    : MySQL
 Source Server Version : 80043
 Source Host           : 114.55.254.123:3306
 Source Schema         : weChat_assistance

 Target Server Type    : MySQL
 Target Server Version : 80043
 File Encoding         : 65001

 Date: 10/10/2025 12:25:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for client_info
-- ----------------------------
DROP TABLE IF EXISTS `client_info`;
CREATE TABLE `client_info`  (
  `mac` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '客户端 MAC 地址',
  `os_version` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作系统版本',
  `client_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '客户端应用名',
  `cpu_version` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'CPU 型号',
  `ip` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '内网/外网 IP',
  `wechat_username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录的微信用户名',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号（可选）',
  `login_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '首次上线时间',
  PRIMARY KEY (`mac`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '客户端基本信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for lic_info
-- ----------------------------
DROP TABLE IF EXISTS `lic_info`;
CREATE TABLE `lic_info`  (
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '手机号',
  `mac` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '客户端 MAC',
  `user_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '-2过期 -1试用 1 1个月 2 1年',
  `begin_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '授权开始时间'
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '授权信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for trade_info
-- ----------------------------
DROP TABLE IF EXISTS `trade_info`;
CREATE TABLE `trade_info`  (
  `out_trade_no` varchar(125) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '订单号',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '手机号',
  `mac` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '客户端 MAC',
  `trade_subject` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '订单主题',
  `trade_create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '订单创建时间',
  `total_amount` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '订单金额',
  `qr_code_url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '订单二维码',
  `trade_payment_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '订单付款时间',
  `trade_payment_info` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '订单付款信息',
  PRIMARY KEY (`out_trade_no`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '订单记录信息' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
