/*
 Navicat Premium Data Transfer

 Source Server         : 114.55.254.123
 Source Server Type    : MySQL
 Source Server Version : 80043
 Source Host           : 114.55.254.123:3306
 Source Schema         : eylink_store

 Target Server Type    : MySQL
 Target Server Version : 80043
 File Encoding         : 65001

 Date: 25/10/2025 19:07:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单号',
  `product_id` int(0) NOT NULL,
  `product_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '产品名称快照',
  `price` decimal(10, 2) NOT NULL COMMENT '单价快照',
  `quantity` int(0) NOT NULL COMMENT '购买数量',
  `total_amount` decimal(10, 2) NOT NULL COMMENT '总金额',
  `customer_email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '客户邮箱',
  `payment_method` enum('wechat','alipay') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'wechat' COMMENT '支付方式',
  `payment_status` enum('pending','paid','failed','expired','refunded') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending' COMMENT '支付状态',
  `order_status` enum('pending','processing','completed','cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending' COMMENT '订单状态',
  `delivery_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '发货内容',
  `delivery_time` timestamp(0) NULL DEFAULT NULL COMMENT '发货时间',
  `payment_time` timestamp(0) NULL DEFAULT NULL COMMENT '支付时间',
  `created_at` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `order_number`(`order_number`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 102 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES (98, 'ORD20251023205341S4ASUK', 1, 'ChatGPT老号3', 4.90, 1, 4.90, '594462206@qq.com', 'wechat', 'paid', 'processing', NULL, NULL, '2025-10-23 20:54:19', '2025-10-23 20:53:41', '2025-10-23 20:54:19');
INSERT INTO `orders` VALUES (99, 'ORD20251023205543E5872X', 1, 'ChatGPT老号3', 4.90, 5, 24.50, '594462206@qq.com', 'wechat', 'pending', 'pending', NULL, NULL, NULL, '2025-10-23 20:55:43', '2025-10-23 20:55:43');
INSERT INTO `orders` VALUES (100, 'ORD202510232057273245TW', 1, 'ChatGPT老号3', 4.90, 5, 24.50, '594462206@qq.com', 'wechat', 'pending', 'pending', NULL, NULL, NULL, '2025-10-23 20:57:27', '2025-10-23 20:57:27');
INSERT INTO `orders` VALUES (101, 'ORD20251023210132JBQI3A', 1, 'ChatGPT老号3', 4.90, 1, 4.90, '594462206@qq.com', 'wechat', 'paid', 'processing', NULL, NULL, '2025-10-23 21:02:17', '2025-10-23 21:01:32', '2025-10-23 21:02:17');

-- ----------------------------
-- Table structure for payments
-- ----------------------------
DROP TABLE IF EXISTS `payments`;
CREATE TABLE `payments`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `order_id` int(0) NOT NULL,
  `payment_method` enum('wechat','alipay') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_amount` decimal(10, 2) NULL DEFAULT 0.00,
  `payment_status` enum('pending','success','failed','expired') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending',
  `transaction_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '第三方交易ID',
  `qr_code_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `expires_at` timestamp(0) NULL DEFAULT NULL COMMENT '支付过期时间',
  `paid_at` timestamp(0) NULL DEFAULT NULL COMMENT '支付完成时间',
  `created_at` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  `payment_number` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `amount` decimal(10, 2) NOT NULL DEFAULT 0.00,
  `qr_code` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `qr_image` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `payment_number`(`payment_number`) USING BTREE,
  INDEX `order_id`(`order_id`) USING BTREE,
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 63 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of payments
-- ----------------------------
INSERT INTO `payments` VALUES (60, 98, 'wechat', 4.90, 'success', '11111111111_12:7F:E5:F2:07:11_2025-10-23 20:53:49.462434', 'https://qr.alipay.com/bax04410yluvm0jfbjh585f7', '2025-10-23 21:08:45', '2025-10-23 20:54:19', '2025-10-23 20:53:45', '2025-10-23 20:54:19', 'PAY202510232053442LGABO', 0.00, 'weixin://wxpay/bizpayurl?pr=PAY202510232053442LGABO', NULL);
INSERT INTO `payments` VALUES (61, 99, 'wechat', 24.50, 'pending', '11111111111_12:7F:E5:F2:07:11_2025-10-23 20:55:56.695147', 'https://qr.alipay.com/bax04888hpim1xstjmel00c1', '2025-10-23 21:10:56', NULL, '2025-10-23 20:55:55', '2025-10-23 20:55:57', 'PAY20251023205555SH1JUS', 0.00, 'weixin://wxpay/bizpayurl?pr=PAY20251023205555SH1JUS', NULL);
INSERT INTO `payments` VALUES (62, 101, 'wechat', 4.90, 'success', '11111111111_12:7F:E5:F2:07:11_2025-10-23 21:01:45.445867', 'https://qr.alipay.com/bax00920bqexxksbene85557', '2025-10-23 21:16:41', '2025-10-23 21:02:17', '2025-10-23 21:01:40', '2025-10-23 21:02:17', 'PAY20251023210140NYHEHH', 0.00, 'weixin://wxpay/bizpayurl?pr=PAY20251023210140NYHEHH', NULL);

-- ----------------------------
-- Table structure for product_features
-- ----------------------------
DROP TABLE IF EXISTS `product_features`;
CREATE TABLE `product_features`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `product_id` int(0) NOT NULL,
  `feature_text` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '特性描述',
  `sort_order` int(0) NULL DEFAULT 0 COMMENT '排序',
  `created_at` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  CONSTRAINT `product_features_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 529 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of product_features
-- ----------------------------
INSERT INTO `product_features` VALUES (1, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-23 08:08:13');
INSERT INTO `product_features` VALUES (2, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-23 08:08:13');
INSERT INTO `product_features` VALUES (3, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-23 08:08:13');
INSERT INTO `product_features` VALUES (4, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-23 08:08:13');
INSERT INTO `product_features` VALUES (5, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-23 08:08:13');
INSERT INTO `product_features` VALUES (6, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-23 08:08:13');
INSERT INTO `product_features` VALUES (7, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-23 16:07:25');
INSERT INTO `product_features` VALUES (8, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-23 16:07:25');
INSERT INTO `product_features` VALUES (9, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-23 16:07:25');
INSERT INTO `product_features` VALUES (10, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-23 16:07:25');
INSERT INTO `product_features` VALUES (11, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-23 16:07:25');
INSERT INTO `product_features` VALUES (12, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-23 16:07:25');
INSERT INTO `product_features` VALUES (13, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-23 16:21:29');
INSERT INTO `product_features` VALUES (14, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-23 16:21:29');
INSERT INTO `product_features` VALUES (15, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-23 16:21:29');
INSERT INTO `product_features` VALUES (16, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-23 16:21:29');
INSERT INTO `product_features` VALUES (17, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-23 16:21:29');
INSERT INTO `product_features` VALUES (18, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-23 16:21:29');
INSERT INTO `product_features` VALUES (19, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-23 16:59:19');
INSERT INTO `product_features` VALUES (20, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-23 16:59:19');
INSERT INTO `product_features` VALUES (21, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-23 16:59:19');
INSERT INTO `product_features` VALUES (22, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-23 16:59:19');
INSERT INTO `product_features` VALUES (23, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-23 16:59:19');
INSERT INTO `product_features` VALUES (24, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-23 16:59:19');
INSERT INTO `product_features` VALUES (25, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-23 17:38:57');
INSERT INTO `product_features` VALUES (26, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-23 17:38:57');
INSERT INTO `product_features` VALUES (27, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-23 17:38:57');
INSERT INTO `product_features` VALUES (28, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-23 17:38:57');
INSERT INTO `product_features` VALUES (29, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-23 17:38:57');
INSERT INTO `product_features` VALUES (30, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-23 17:38:57');
INSERT INTO `product_features` VALUES (31, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-23 17:40:05');
INSERT INTO `product_features` VALUES (32, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-23 17:40:05');
INSERT INTO `product_features` VALUES (33, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-23 17:40:05');
INSERT INTO `product_features` VALUES (34, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-23 17:40:05');
INSERT INTO `product_features` VALUES (35, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-23 17:40:05');
INSERT INTO `product_features` VALUES (36, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-23 17:40:05');
INSERT INTO `product_features` VALUES (37, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-23 17:51:45');
INSERT INTO `product_features` VALUES (38, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-23 17:51:45');
INSERT INTO `product_features` VALUES (39, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-23 17:51:45');
INSERT INTO `product_features` VALUES (40, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-23 17:51:45');
INSERT INTO `product_features` VALUES (41, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-23 17:51:45');
INSERT INTO `product_features` VALUES (42, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-23 17:51:45');
INSERT INTO `product_features` VALUES (43, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-23 18:15:31');
INSERT INTO `product_features` VALUES (44, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-23 18:15:31');
INSERT INTO `product_features` VALUES (45, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-23 18:15:31');
INSERT INTO `product_features` VALUES (46, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-23 18:15:31');
INSERT INTO `product_features` VALUES (47, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-23 18:15:31');
INSERT INTO `product_features` VALUES (48, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-23 18:15:31');
INSERT INTO `product_features` VALUES (49, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-23 18:46:14');
INSERT INTO `product_features` VALUES (50, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-23 18:46:14');
INSERT INTO `product_features` VALUES (51, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-23 18:46:14');
INSERT INTO `product_features` VALUES (52, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-23 18:46:14');
INSERT INTO `product_features` VALUES (53, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-23 18:46:14');
INSERT INTO `product_features` VALUES (54, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-23 18:46:14');
INSERT INTO `product_features` VALUES (55, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-25 23:54:13');
INSERT INTO `product_features` VALUES (56, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-25 23:54:13');
INSERT INTO `product_features` VALUES (57, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-25 23:54:13');
INSERT INTO `product_features` VALUES (58, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-25 23:54:13');
INSERT INTO `product_features` VALUES (59, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-25 23:54:13');
INSERT INTO `product_features` VALUES (60, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-25 23:54:13');
INSERT INTO `product_features` VALUES (61, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 00:03:00');
INSERT INTO `product_features` VALUES (62, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 00:03:00');
INSERT INTO `product_features` VALUES (63, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 00:03:00');
INSERT INTO `product_features` VALUES (64, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 00:03:00');
INSERT INTO `product_features` VALUES (65, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 00:03:00');
INSERT INTO `product_features` VALUES (66, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 00:03:00');
INSERT INTO `product_features` VALUES (67, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 00:10:55');
INSERT INTO `product_features` VALUES (68, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 00:10:55');
INSERT INTO `product_features` VALUES (69, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 00:10:55');
INSERT INTO `product_features` VALUES (70, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 00:10:55');
INSERT INTO `product_features` VALUES (71, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 00:10:55');
INSERT INTO `product_features` VALUES (72, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 00:10:55');
INSERT INTO `product_features` VALUES (73, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 07:42:39');
INSERT INTO `product_features` VALUES (74, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 07:42:39');
INSERT INTO `product_features` VALUES (75, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 07:42:39');
INSERT INTO `product_features` VALUES (76, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 07:42:39');
INSERT INTO `product_features` VALUES (77, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 07:42:39');
INSERT INTO `product_features` VALUES (78, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 07:42:39');
INSERT INTO `product_features` VALUES (79, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 08:32:59');
INSERT INTO `product_features` VALUES (80, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 08:32:59');
INSERT INTO `product_features` VALUES (81, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 08:32:59');
INSERT INTO `product_features` VALUES (82, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 08:32:59');
INSERT INTO `product_features` VALUES (83, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 08:32:59');
INSERT INTO `product_features` VALUES (84, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 08:32:59');
INSERT INTO `product_features` VALUES (85, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 13:32:11');
INSERT INTO `product_features` VALUES (86, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 13:32:11');
INSERT INTO `product_features` VALUES (87, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 13:32:11');
INSERT INTO `product_features` VALUES (88, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 13:32:11');
INSERT INTO `product_features` VALUES (89, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 13:32:11');
INSERT INTO `product_features` VALUES (90, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 13:32:11');
INSERT INTO `product_features` VALUES (91, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 13:38:11');
INSERT INTO `product_features` VALUES (92, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 13:38:11');
INSERT INTO `product_features` VALUES (93, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 13:38:11');
INSERT INTO `product_features` VALUES (94, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 13:38:11');
INSERT INTO `product_features` VALUES (95, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 13:38:11');
INSERT INTO `product_features` VALUES (96, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 13:38:11');
INSERT INTO `product_features` VALUES (97, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 13:53:41');
INSERT INTO `product_features` VALUES (98, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 13:53:41');
INSERT INTO `product_features` VALUES (99, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 13:53:41');
INSERT INTO `product_features` VALUES (100, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 13:53:41');
INSERT INTO `product_features` VALUES (101, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 13:53:41');
INSERT INTO `product_features` VALUES (102, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 13:53:41');
INSERT INTO `product_features` VALUES (103, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 13:57:21');
INSERT INTO `product_features` VALUES (104, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 13:57:21');
INSERT INTO `product_features` VALUES (105, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 13:57:21');
INSERT INTO `product_features` VALUES (106, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 13:57:21');
INSERT INTO `product_features` VALUES (107, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 13:57:21');
INSERT INTO `product_features` VALUES (108, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 13:57:21');
INSERT INTO `product_features` VALUES (109, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 19:41:09');
INSERT INTO `product_features` VALUES (110, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 19:41:09');
INSERT INTO `product_features` VALUES (111, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 19:41:09');
INSERT INTO `product_features` VALUES (112, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 19:41:09');
INSERT INTO `product_features` VALUES (113, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 19:41:09');
INSERT INTO `product_features` VALUES (114, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 19:41:09');
INSERT INTO `product_features` VALUES (115, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 19:42:11');
INSERT INTO `product_features` VALUES (116, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 19:42:11');
INSERT INTO `product_features` VALUES (117, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 19:42:11');
INSERT INTO `product_features` VALUES (118, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 19:42:11');
INSERT INTO `product_features` VALUES (119, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 19:42:11');
INSERT INTO `product_features` VALUES (120, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 19:42:11');
INSERT INTO `product_features` VALUES (121, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 19:44:04');
INSERT INTO `product_features` VALUES (122, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 19:44:04');
INSERT INTO `product_features` VALUES (123, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 19:44:04');
INSERT INTO `product_features` VALUES (124, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 19:44:04');
INSERT INTO `product_features` VALUES (125, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 19:44:04');
INSERT INTO `product_features` VALUES (126, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 19:44:04');
INSERT INTO `product_features` VALUES (127, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 19:44:57');
INSERT INTO `product_features` VALUES (128, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 19:44:57');
INSERT INTO `product_features` VALUES (129, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 19:44:57');
INSERT INTO `product_features` VALUES (130, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 19:44:57');
INSERT INTO `product_features` VALUES (131, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 19:44:57');
INSERT INTO `product_features` VALUES (132, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 19:44:57');
INSERT INTO `product_features` VALUES (133, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 19:56:30');
INSERT INTO `product_features` VALUES (134, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 19:56:30');
INSERT INTO `product_features` VALUES (135, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 19:56:30');
INSERT INTO `product_features` VALUES (136, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 19:56:30');
INSERT INTO `product_features` VALUES (137, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 19:56:30');
INSERT INTO `product_features` VALUES (138, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 19:56:30');
INSERT INTO `product_features` VALUES (139, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 20:08:19');
INSERT INTO `product_features` VALUES (140, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 20:08:19');
INSERT INTO `product_features` VALUES (141, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 20:08:19');
INSERT INTO `product_features` VALUES (142, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 20:08:19');
INSERT INTO `product_features` VALUES (143, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 20:08:19');
INSERT INTO `product_features` VALUES (144, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 20:08:19');
INSERT INTO `product_features` VALUES (145, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 20:11:37');
INSERT INTO `product_features` VALUES (146, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 20:11:37');
INSERT INTO `product_features` VALUES (147, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 20:11:37');
INSERT INTO `product_features` VALUES (148, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 20:11:37');
INSERT INTO `product_features` VALUES (149, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 20:11:37');
INSERT INTO `product_features` VALUES (150, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 20:11:37');
INSERT INTO `product_features` VALUES (151, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 20:25:37');
INSERT INTO `product_features` VALUES (152, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 20:25:37');
INSERT INTO `product_features` VALUES (153, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 20:25:37');
INSERT INTO `product_features` VALUES (154, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 20:25:37');
INSERT INTO `product_features` VALUES (155, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 20:25:37');
INSERT INTO `product_features` VALUES (156, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 20:25:37');
INSERT INTO `product_features` VALUES (157, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 20:27:37');
INSERT INTO `product_features` VALUES (158, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 20:27:37');
INSERT INTO `product_features` VALUES (159, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 20:27:37');
INSERT INTO `product_features` VALUES (160, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 20:27:37');
INSERT INTO `product_features` VALUES (161, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 20:27:37');
INSERT INTO `product_features` VALUES (162, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 20:27:37');
INSERT INTO `product_features` VALUES (163, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 20:27:51');
INSERT INTO `product_features` VALUES (164, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 20:27:51');
INSERT INTO `product_features` VALUES (165, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 20:27:51');
INSERT INTO `product_features` VALUES (166, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 20:27:51');
INSERT INTO `product_features` VALUES (167, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 20:27:51');
INSERT INTO `product_features` VALUES (168, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 20:27:51');
INSERT INTO `product_features` VALUES (169, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 20:30:39');
INSERT INTO `product_features` VALUES (170, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 20:30:39');
INSERT INTO `product_features` VALUES (171, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 20:30:39');
INSERT INTO `product_features` VALUES (172, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 20:30:39');
INSERT INTO `product_features` VALUES (173, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 20:30:39');
INSERT INTO `product_features` VALUES (174, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 20:30:39');
INSERT INTO `product_features` VALUES (175, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 20:34:53');
INSERT INTO `product_features` VALUES (176, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 20:34:53');
INSERT INTO `product_features` VALUES (177, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 20:34:53');
INSERT INTO `product_features` VALUES (178, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 20:34:53');
INSERT INTO `product_features` VALUES (179, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 20:34:53');
INSERT INTO `product_features` VALUES (180, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 20:34:53');
INSERT INTO `product_features` VALUES (181, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 20:36:10');
INSERT INTO `product_features` VALUES (182, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 20:36:10');
INSERT INTO `product_features` VALUES (183, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 20:36:10');
INSERT INTO `product_features` VALUES (184, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 20:36:10');
INSERT INTO `product_features` VALUES (185, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 20:36:10');
INSERT INTO `product_features` VALUES (186, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 20:36:10');
INSERT INTO `product_features` VALUES (187, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 20:38:41');
INSERT INTO `product_features` VALUES (188, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 20:38:41');
INSERT INTO `product_features` VALUES (189, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 20:38:41');
INSERT INTO `product_features` VALUES (190, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 20:38:41');
INSERT INTO `product_features` VALUES (191, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 20:38:41');
INSERT INTO `product_features` VALUES (192, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 20:38:41');
INSERT INTO `product_features` VALUES (193, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 20:44:10');
INSERT INTO `product_features` VALUES (194, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 20:44:10');
INSERT INTO `product_features` VALUES (195, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 20:44:10');
INSERT INTO `product_features` VALUES (196, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 20:44:10');
INSERT INTO `product_features` VALUES (197, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 20:44:10');
INSERT INTO `product_features` VALUES (198, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 20:44:10');
INSERT INTO `product_features` VALUES (199, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 21:06:17');
INSERT INTO `product_features` VALUES (200, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 21:06:17');
INSERT INTO `product_features` VALUES (201, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 21:06:17');
INSERT INTO `product_features` VALUES (202, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 21:06:17');
INSERT INTO `product_features` VALUES (203, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 21:06:17');
INSERT INTO `product_features` VALUES (204, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 21:06:17');
INSERT INTO `product_features` VALUES (205, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 21:22:52');
INSERT INTO `product_features` VALUES (206, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 21:22:52');
INSERT INTO `product_features` VALUES (207, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 21:22:52');
INSERT INTO `product_features` VALUES (208, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 21:22:52');
INSERT INTO `product_features` VALUES (209, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 21:22:52');
INSERT INTO `product_features` VALUES (210, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 21:22:52');
INSERT INTO `product_features` VALUES (211, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 21:24:21');
INSERT INTO `product_features` VALUES (212, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 21:24:21');
INSERT INTO `product_features` VALUES (213, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 21:24:21');
INSERT INTO `product_features` VALUES (214, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 21:24:21');
INSERT INTO `product_features` VALUES (215, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 21:24:21');
INSERT INTO `product_features` VALUES (216, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 21:24:21');
INSERT INTO `product_features` VALUES (217, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 21:25:30');
INSERT INTO `product_features` VALUES (218, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 21:25:30');
INSERT INTO `product_features` VALUES (219, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 21:25:30');
INSERT INTO `product_features` VALUES (220, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 21:25:30');
INSERT INTO `product_features` VALUES (221, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 21:25:30');
INSERT INTO `product_features` VALUES (222, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 21:25:30');
INSERT INTO `product_features` VALUES (223, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 21:27:07');
INSERT INTO `product_features` VALUES (224, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 21:27:07');
INSERT INTO `product_features` VALUES (225, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 21:27:07');
INSERT INTO `product_features` VALUES (226, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 21:27:07');
INSERT INTO `product_features` VALUES (227, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 21:27:07');
INSERT INTO `product_features` VALUES (228, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 21:27:07');
INSERT INTO `product_features` VALUES (229, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 21:31:59');
INSERT INTO `product_features` VALUES (230, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 21:31:59');
INSERT INTO `product_features` VALUES (231, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 21:31:59');
INSERT INTO `product_features` VALUES (232, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 21:31:59');
INSERT INTO `product_features` VALUES (233, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 21:31:59');
INSERT INTO `product_features` VALUES (234, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 21:31:59');
INSERT INTO `product_features` VALUES (235, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 21:39:34');
INSERT INTO `product_features` VALUES (236, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 21:39:34');
INSERT INTO `product_features` VALUES (237, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 21:39:34');
INSERT INTO `product_features` VALUES (238, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 21:39:34');
INSERT INTO `product_features` VALUES (239, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 21:39:34');
INSERT INTO `product_features` VALUES (240, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 21:39:34');
INSERT INTO `product_features` VALUES (241, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-26 22:30:53');
INSERT INTO `product_features` VALUES (242, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-26 22:30:53');
INSERT INTO `product_features` VALUES (243, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-26 22:30:53');
INSERT INTO `product_features` VALUES (244, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-26 22:30:53');
INSERT INTO `product_features` VALUES (245, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-26 22:30:53');
INSERT INTO `product_features` VALUES (246, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-26 22:30:53');
INSERT INTO `product_features` VALUES (247, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 08:00:31');
INSERT INTO `product_features` VALUES (248, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 08:00:31');
INSERT INTO `product_features` VALUES (249, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 08:00:31');
INSERT INTO `product_features` VALUES (250, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 08:00:31');
INSERT INTO `product_features` VALUES (251, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 08:00:31');
INSERT INTO `product_features` VALUES (252, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 08:00:31');
INSERT INTO `product_features` VALUES (253, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 12:34:32');
INSERT INTO `product_features` VALUES (254, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 12:34:32');
INSERT INTO `product_features` VALUES (255, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 12:34:32');
INSERT INTO `product_features` VALUES (256, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 12:34:32');
INSERT INTO `product_features` VALUES (257, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 12:34:32');
INSERT INTO `product_features` VALUES (258, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 12:34:32');
INSERT INTO `product_features` VALUES (259, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 15:02:31');
INSERT INTO `product_features` VALUES (260, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 15:02:31');
INSERT INTO `product_features` VALUES (261, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 15:02:31');
INSERT INTO `product_features` VALUES (262, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 15:02:31');
INSERT INTO `product_features` VALUES (263, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 15:02:31');
INSERT INTO `product_features` VALUES (264, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 15:02:31');
INSERT INTO `product_features` VALUES (265, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 19:40:18');
INSERT INTO `product_features` VALUES (266, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 19:40:18');
INSERT INTO `product_features` VALUES (267, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 19:40:18');
INSERT INTO `product_features` VALUES (268, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 19:40:18');
INSERT INTO `product_features` VALUES (269, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 19:40:18');
INSERT INTO `product_features` VALUES (270, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 19:40:18');
INSERT INTO `product_features` VALUES (271, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 19:51:41');
INSERT INTO `product_features` VALUES (272, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 19:51:41');
INSERT INTO `product_features` VALUES (273, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 19:51:41');
INSERT INTO `product_features` VALUES (274, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 19:51:41');
INSERT INTO `product_features` VALUES (275, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 19:51:41');
INSERT INTO `product_features` VALUES (276, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 19:51:41');
INSERT INTO `product_features` VALUES (277, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 19:54:20');
INSERT INTO `product_features` VALUES (278, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 19:54:20');
INSERT INTO `product_features` VALUES (279, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 19:54:20');
INSERT INTO `product_features` VALUES (280, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 19:54:20');
INSERT INTO `product_features` VALUES (281, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 19:54:20');
INSERT INTO `product_features` VALUES (282, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 19:54:20');
INSERT INTO `product_features` VALUES (283, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 19:58:54');
INSERT INTO `product_features` VALUES (284, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 19:58:54');
INSERT INTO `product_features` VALUES (285, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 19:58:54');
INSERT INTO `product_features` VALUES (286, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 19:58:54');
INSERT INTO `product_features` VALUES (287, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 19:58:54');
INSERT INTO `product_features` VALUES (288, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 19:58:54');
INSERT INTO `product_features` VALUES (289, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 19:59:41');
INSERT INTO `product_features` VALUES (290, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 19:59:41');
INSERT INTO `product_features` VALUES (291, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 19:59:41');
INSERT INTO `product_features` VALUES (292, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 19:59:41');
INSERT INTO `product_features` VALUES (293, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 19:59:41');
INSERT INTO `product_features` VALUES (294, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 19:59:41');
INSERT INTO `product_features` VALUES (295, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 20:00:12');
INSERT INTO `product_features` VALUES (296, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 20:00:12');
INSERT INTO `product_features` VALUES (297, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 20:00:12');
INSERT INTO `product_features` VALUES (298, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 20:00:12');
INSERT INTO `product_features` VALUES (299, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 20:00:12');
INSERT INTO `product_features` VALUES (300, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 20:00:12');
INSERT INTO `product_features` VALUES (301, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 20:01:00');
INSERT INTO `product_features` VALUES (302, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 20:01:00');
INSERT INTO `product_features` VALUES (303, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 20:01:00');
INSERT INTO `product_features` VALUES (304, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 20:01:00');
INSERT INTO `product_features` VALUES (305, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 20:01:00');
INSERT INTO `product_features` VALUES (306, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 20:01:00');
INSERT INTO `product_features` VALUES (307, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 20:01:39');
INSERT INTO `product_features` VALUES (308, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 20:01:39');
INSERT INTO `product_features` VALUES (309, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 20:01:39');
INSERT INTO `product_features` VALUES (310, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 20:01:39');
INSERT INTO `product_features` VALUES (311, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 20:01:39');
INSERT INTO `product_features` VALUES (312, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 20:01:39');
INSERT INTO `product_features` VALUES (313, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 20:04:12');
INSERT INTO `product_features` VALUES (314, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 20:04:12');
INSERT INTO `product_features` VALUES (315, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 20:04:12');
INSERT INTO `product_features` VALUES (316, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 20:04:12');
INSERT INTO `product_features` VALUES (317, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 20:04:12');
INSERT INTO `product_features` VALUES (318, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 20:04:12');
INSERT INTO `product_features` VALUES (319, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 20:04:38');
INSERT INTO `product_features` VALUES (320, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 20:04:38');
INSERT INTO `product_features` VALUES (321, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 20:04:38');
INSERT INTO `product_features` VALUES (322, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 20:04:38');
INSERT INTO `product_features` VALUES (323, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 20:04:38');
INSERT INTO `product_features` VALUES (324, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 20:04:38');
INSERT INTO `product_features` VALUES (325, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 20:09:59');
INSERT INTO `product_features` VALUES (326, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 20:09:59');
INSERT INTO `product_features` VALUES (327, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 20:09:59');
INSERT INTO `product_features` VALUES (328, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 20:09:59');
INSERT INTO `product_features` VALUES (329, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 20:09:59');
INSERT INTO `product_features` VALUES (330, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 20:09:59');
INSERT INTO `product_features` VALUES (331, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 20:20:30');
INSERT INTO `product_features` VALUES (332, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 20:20:30');
INSERT INTO `product_features` VALUES (333, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 20:20:30');
INSERT INTO `product_features` VALUES (334, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 20:20:30');
INSERT INTO `product_features` VALUES (335, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 20:20:30');
INSERT INTO `product_features` VALUES (336, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 20:20:30');
INSERT INTO `product_features` VALUES (337, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 20:26:11');
INSERT INTO `product_features` VALUES (338, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 20:26:11');
INSERT INTO `product_features` VALUES (339, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 20:26:11');
INSERT INTO `product_features` VALUES (340, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 20:26:11');
INSERT INTO `product_features` VALUES (341, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 20:26:11');
INSERT INTO `product_features` VALUES (342, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 20:26:11');
INSERT INTO `product_features` VALUES (343, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 21:16:23');
INSERT INTO `product_features` VALUES (344, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 21:16:23');
INSERT INTO `product_features` VALUES (345, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 21:16:23');
INSERT INTO `product_features` VALUES (346, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 21:16:23');
INSERT INTO `product_features` VALUES (347, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 21:16:23');
INSERT INTO `product_features` VALUES (348, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 21:16:23');
INSERT INTO `product_features` VALUES (349, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-27 21:18:07');
INSERT INTO `product_features` VALUES (350, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-27 21:18:07');
INSERT INTO `product_features` VALUES (351, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-27 21:18:07');
INSERT INTO `product_features` VALUES (352, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-27 21:18:07');
INSERT INTO `product_features` VALUES (353, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-27 21:18:07');
INSERT INTO `product_features` VALUES (354, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-27 21:18:07');
INSERT INTO `product_features` VALUES (355, 1, '购买25次或以上立减：4.8¥', 1, '2025-08-28 22:08:36');
INSERT INTO `product_features` VALUES (356, 1, '购买25次或以上立减：4.7¥', 2, '2025-08-28 22:08:36');
INSERT INTO `product_features` VALUES (357, 1, '购买50次或以上立减：4.6¥', 3, '2025-08-28 22:08:36');
INSERT INTO `product_features` VALUES (358, 1, '购买100次或以上立减：4.5¥', 4, '2025-08-28 22:08:36');
INSERT INTO `product_features` VALUES (359, 1, '购买200次或以上立减：4.4¥', 5, '2025-08-28 22:08:36');
INSERT INTO `product_features` VALUES (360, 1, '购买500次或以上立减：4.2¥', 6, '2025-08-28 22:08:36');
INSERT INTO `product_features` VALUES (361, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-09 11:25:05');
INSERT INTO `product_features` VALUES (362, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-09 11:25:05');
INSERT INTO `product_features` VALUES (363, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-09 11:25:05');
INSERT INTO `product_features` VALUES (364, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-09 11:25:05');
INSERT INTO `product_features` VALUES (365, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-09 11:25:05');
INSERT INTO `product_features` VALUES (366, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-09 11:25:05');
INSERT INTO `product_features` VALUES (367, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-09 11:29:32');
INSERT INTO `product_features` VALUES (368, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-09 11:29:32');
INSERT INTO `product_features` VALUES (369, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-09 11:29:32');
INSERT INTO `product_features` VALUES (370, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-09 11:29:32');
INSERT INTO `product_features` VALUES (371, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-09 11:29:32');
INSERT INTO `product_features` VALUES (372, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-09 11:29:32');
INSERT INTO `product_features` VALUES (373, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-09 11:31:33');
INSERT INTO `product_features` VALUES (374, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-09 11:31:33');
INSERT INTO `product_features` VALUES (375, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-09 11:31:33');
INSERT INTO `product_features` VALUES (376, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-09 11:31:33');
INSERT INTO `product_features` VALUES (377, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-09 11:31:33');
INSERT INTO `product_features` VALUES (378, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-09 11:31:33');
INSERT INTO `product_features` VALUES (379, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-09 11:37:14');
INSERT INTO `product_features` VALUES (380, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-09 11:37:14');
INSERT INTO `product_features` VALUES (381, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-09 11:37:14');
INSERT INTO `product_features` VALUES (382, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-09 11:37:14');
INSERT INTO `product_features` VALUES (383, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-09 11:37:14');
INSERT INTO `product_features` VALUES (384, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-09 11:37:14');
INSERT INTO `product_features` VALUES (385, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-09 11:40:38');
INSERT INTO `product_features` VALUES (386, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-09 11:40:38');
INSERT INTO `product_features` VALUES (387, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-09 11:40:38');
INSERT INTO `product_features` VALUES (388, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-09 11:40:38');
INSERT INTO `product_features` VALUES (389, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-09 11:40:38');
INSERT INTO `product_features` VALUES (390, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-09 11:40:38');
INSERT INTO `product_features` VALUES (391, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-09 14:20:33');
INSERT INTO `product_features` VALUES (392, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-09 14:20:33');
INSERT INTO `product_features` VALUES (393, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-09 14:20:33');
INSERT INTO `product_features` VALUES (394, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-09 14:20:33');
INSERT INTO `product_features` VALUES (395, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-09 14:20:33');
INSERT INTO `product_features` VALUES (396, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-09 14:20:33');
INSERT INTO `product_features` VALUES (397, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-13 16:57:52');
INSERT INTO `product_features` VALUES (398, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-13 16:57:52');
INSERT INTO `product_features` VALUES (399, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-13 16:57:52');
INSERT INTO `product_features` VALUES (400, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-13 16:57:52');
INSERT INTO `product_features` VALUES (401, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-13 16:57:52');
INSERT INTO `product_features` VALUES (402, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-13 16:57:52');
INSERT INTO `product_features` VALUES (403, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-13 17:15:22');
INSERT INTO `product_features` VALUES (404, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-13 17:15:22');
INSERT INTO `product_features` VALUES (405, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-13 17:15:22');
INSERT INTO `product_features` VALUES (406, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-13 17:15:22');
INSERT INTO `product_features` VALUES (407, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-13 17:15:22');
INSERT INTO `product_features` VALUES (408, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-13 17:15:22');
INSERT INTO `product_features` VALUES (409, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-13 17:57:44');
INSERT INTO `product_features` VALUES (410, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-13 17:57:44');
INSERT INTO `product_features` VALUES (411, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-13 17:57:44');
INSERT INTO `product_features` VALUES (412, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-13 17:57:44');
INSERT INTO `product_features` VALUES (413, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-13 17:57:44');
INSERT INTO `product_features` VALUES (414, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-13 17:57:44');
INSERT INTO `product_features` VALUES (415, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-13 17:58:27');
INSERT INTO `product_features` VALUES (416, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-13 17:58:27');
INSERT INTO `product_features` VALUES (417, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-13 17:58:27');
INSERT INTO `product_features` VALUES (418, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-13 17:58:27');
INSERT INTO `product_features` VALUES (419, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-13 17:58:27');
INSERT INTO `product_features` VALUES (420, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-13 17:58:27');
INSERT INTO `product_features` VALUES (421, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 14:52:31');
INSERT INTO `product_features` VALUES (422, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 14:52:31');
INSERT INTO `product_features` VALUES (423, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 14:52:31');
INSERT INTO `product_features` VALUES (424, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 14:52:31');
INSERT INTO `product_features` VALUES (425, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 14:52:31');
INSERT INTO `product_features` VALUES (426, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 14:52:31');
INSERT INTO `product_features` VALUES (427, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 14:53:17');
INSERT INTO `product_features` VALUES (428, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 14:53:17');
INSERT INTO `product_features` VALUES (429, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 14:53:17');
INSERT INTO `product_features` VALUES (430, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 14:53:17');
INSERT INTO `product_features` VALUES (431, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 14:53:17');
INSERT INTO `product_features` VALUES (432, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 14:53:17');
INSERT INTO `product_features` VALUES (433, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 14:59:44');
INSERT INTO `product_features` VALUES (434, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 14:59:44');
INSERT INTO `product_features` VALUES (435, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 14:59:44');
INSERT INTO `product_features` VALUES (436, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 14:59:44');
INSERT INTO `product_features` VALUES (437, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 14:59:44');
INSERT INTO `product_features` VALUES (438, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 14:59:44');
INSERT INTO `product_features` VALUES (439, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 15:00:15');
INSERT INTO `product_features` VALUES (440, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 15:00:15');
INSERT INTO `product_features` VALUES (441, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 15:00:15');
INSERT INTO `product_features` VALUES (442, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 15:00:15');
INSERT INTO `product_features` VALUES (443, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 15:00:15');
INSERT INTO `product_features` VALUES (444, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 15:00:15');
INSERT INTO `product_features` VALUES (445, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 15:02:39');
INSERT INTO `product_features` VALUES (446, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 15:02:39');
INSERT INTO `product_features` VALUES (447, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 15:02:39');
INSERT INTO `product_features` VALUES (448, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 15:02:39');
INSERT INTO `product_features` VALUES (449, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 15:02:39');
INSERT INTO `product_features` VALUES (450, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 15:02:39');
INSERT INTO `product_features` VALUES (451, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 15:03:41');
INSERT INTO `product_features` VALUES (452, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 15:03:41');
INSERT INTO `product_features` VALUES (453, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 15:03:41');
INSERT INTO `product_features` VALUES (454, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 15:03:41');
INSERT INTO `product_features` VALUES (455, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 15:03:41');
INSERT INTO `product_features` VALUES (456, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 15:03:41');
INSERT INTO `product_features` VALUES (457, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 15:05:53');
INSERT INTO `product_features` VALUES (458, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 15:05:53');
INSERT INTO `product_features` VALUES (459, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 15:05:53');
INSERT INTO `product_features` VALUES (460, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 15:05:53');
INSERT INTO `product_features` VALUES (461, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 15:05:53');
INSERT INTO `product_features` VALUES (462, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 15:05:53');
INSERT INTO `product_features` VALUES (463, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 15:06:41');
INSERT INTO `product_features` VALUES (464, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 15:06:41');
INSERT INTO `product_features` VALUES (465, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 15:06:41');
INSERT INTO `product_features` VALUES (466, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 15:06:41');
INSERT INTO `product_features` VALUES (467, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 15:06:41');
INSERT INTO `product_features` VALUES (468, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 15:06:41');
INSERT INTO `product_features` VALUES (469, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 15:13:25');
INSERT INTO `product_features` VALUES (470, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 15:13:25');
INSERT INTO `product_features` VALUES (471, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 15:13:25');
INSERT INTO `product_features` VALUES (472, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 15:13:25');
INSERT INTO `product_features` VALUES (473, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 15:13:25');
INSERT INTO `product_features` VALUES (474, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 15:13:25');
INSERT INTO `product_features` VALUES (475, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 16:44:05');
INSERT INTO `product_features` VALUES (476, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 16:44:05');
INSERT INTO `product_features` VALUES (477, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 16:44:05');
INSERT INTO `product_features` VALUES (478, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 16:44:05');
INSERT INTO `product_features` VALUES (479, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 16:44:05');
INSERT INTO `product_features` VALUES (480, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 16:44:05');
INSERT INTO `product_features` VALUES (481, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 17:11:41');
INSERT INTO `product_features` VALUES (482, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 17:11:41');
INSERT INTO `product_features` VALUES (483, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 17:11:41');
INSERT INTO `product_features` VALUES (484, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 17:11:41');
INSERT INTO `product_features` VALUES (485, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 17:11:41');
INSERT INTO `product_features` VALUES (486, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 17:11:41');
INSERT INTO `product_features` VALUES (487, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-14 17:12:11');
INSERT INTO `product_features` VALUES (488, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-14 17:12:11');
INSERT INTO `product_features` VALUES (489, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-14 17:12:11');
INSERT INTO `product_features` VALUES (490, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-14 17:12:11');
INSERT INTO `product_features` VALUES (491, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-14 17:12:11');
INSERT INTO `product_features` VALUES (492, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-14 17:12:11');
INSERT INTO `product_features` VALUES (493, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-15 20:46:36');
INSERT INTO `product_features` VALUES (494, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-15 20:46:36');
INSERT INTO `product_features` VALUES (495, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-15 20:46:36');
INSERT INTO `product_features` VALUES (496, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-15 20:46:36');
INSERT INTO `product_features` VALUES (497, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-15 20:46:36');
INSERT INTO `product_features` VALUES (498, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-15 20:46:36');
INSERT INTO `product_features` VALUES (499, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-23 20:12:51');
INSERT INTO `product_features` VALUES (500, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-23 20:12:51');
INSERT INTO `product_features` VALUES (501, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-23 20:12:51');
INSERT INTO `product_features` VALUES (502, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-23 20:12:51');
INSERT INTO `product_features` VALUES (503, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-23 20:12:51');
INSERT INTO `product_features` VALUES (504, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-23 20:12:51');
INSERT INTO `product_features` VALUES (505, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-23 20:12:52');
INSERT INTO `product_features` VALUES (506, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-23 20:12:52');
INSERT INTO `product_features` VALUES (507, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-23 20:12:52');
INSERT INTO `product_features` VALUES (508, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-23 20:12:52');
INSERT INTO `product_features` VALUES (509, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-23 20:12:52');
INSERT INTO `product_features` VALUES (510, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-23 20:12:52');
INSERT INTO `product_features` VALUES (511, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-23 20:17:28');
INSERT INTO `product_features` VALUES (512, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-23 20:17:28');
INSERT INTO `product_features` VALUES (513, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-23 20:17:28');
INSERT INTO `product_features` VALUES (514, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-23 20:17:28');
INSERT INTO `product_features` VALUES (515, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-23 20:17:28');
INSERT INTO `product_features` VALUES (516, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-23 20:17:28');
INSERT INTO `product_features` VALUES (517, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-23 20:20:38');
INSERT INTO `product_features` VALUES (518, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-23 20:20:38');
INSERT INTO `product_features` VALUES (519, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-23 20:20:38');
INSERT INTO `product_features` VALUES (520, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-23 20:20:38');
INSERT INTO `product_features` VALUES (521, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-23 20:20:38');
INSERT INTO `product_features` VALUES (522, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-23 20:20:38');
INSERT INTO `product_features` VALUES (523, 1, '购买25次或以上立减：4.8¥', 1, '2025-10-23 20:22:07');
INSERT INTO `product_features` VALUES (524, 1, '购买25次或以上立减：4.7¥', 2, '2025-10-23 20:22:07');
INSERT INTO `product_features` VALUES (525, 1, '购买50次或以上立减：4.6¥', 3, '2025-10-23 20:22:07');
INSERT INTO `product_features` VALUES (526, 1, '购买100次或以上立减：4.5¥', 4, '2025-10-23 20:22:07');
INSERT INTO `product_features` VALUES (527, 1, '购买200次或以上立减：4.4¥', 5, '2025-10-23 20:22:07');
INSERT INTO `product_features` VALUES (528, 1, '购买500次或以上立减：4.2¥', 6, '2025-10-23 20:22:07');

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '产品名称',
  `price` decimal(10, 2) NOT NULL COMMENT '价格',
  `stock` int(0) NOT NULL DEFAULT 0 COMMENT '库存数量',
  `image` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '产品图片URL',
  `is_auto_delivery` tinyint(1) NULL DEFAULT 1 COMMENT '是否自动发货',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '产品描述',
  `delivery_format` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '发货格式',
  `login_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '登录地址',
  `status` enum('active','inactive') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'active' COMMENT '产品状态',
  `created_at` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES (1, 'ChatGPT老号3', 4.90, 791, 'https://ext.same-assets.com/754627011/850038464.png', 1, '<h3>半年老号的优势：</h3><p><strong>优势：不会因为用原因封号（如果注册有问题，存在不到现在）</strong></p><p><strong>劣势：写代码用的敏感过期（可以ChatGPT，不能Playground，不能api）</strong></p><h3>问：可以用多久？我看你价保7天，只能用7天吗？</h3><p><strong>答：只要不封号，可以一直用。</strong></p><div class=\"highlight\"><h3>\"发货格式：账号--密码--教程\"</h3><p><strong>因为是半年老号，注册赠送额度过期</strong></p><p><strong>独享，可以改密码，可以改邮箱密码</strong></p><p><strong>微软邮，非自建，安全！</strong></p></div>', '账号----密码----教程', 'edu.eylink.cn', 'active', '2025-08-23 08:08:13', '2025-10-23 21:01:32');
INSERT INTO `products` VALUES (3, 'ChatGPT Plus', 160.00, 1, 'https://ext.same-assets.com/754627011/598274620.png', 1, '<p><strong>这是网页登录之后问问题，需要用key就买12元的</strong></p><p><strong>支持 gpt-5，o3，o1，联网</strong></p><p><strong>登录方法：edu.eylink.cn</strong></p><p><strong>发货格式：账号----密码</strong></p><h3>Plus优势:</h3><p>1、充值Plus原价消费20刀，可提供消费记录</p><p>2、原价 20 刀合计 140，贵的 20 元是利润+售后</p><p>3、售后可以更换可以退款</p><p>4、可以改openai密码，可以改邮箱密码</p><p>5、只能网页提问，没有 api</p>', '账号----密码', 'edu.eylink.cn', 'active', '2025-08-23 08:08:13', '2025-08-23 08:08:13');
INSERT INTO `products` VALUES (5, 'Gemini_转发 API 全模型', 14.00, 32, 'https://ext.same-assets.com/754627011/1868408872.png', 1, '14元 / 10万', 'API密钥', 'api.gemini.com', 'active', '2025-08-23 08:08:13', '2025-10-15 20:35:36');
INSERT INTO `products` VALUES (6, 'openai_gpt_5转发 API', 12.00, 0, 'https://ext.same-assets.com/754627011/854271483.png', 1, '支持 gpt-5 OpenAI 版本 12元 / 10万', 'API密钥', 'api.openai.com', 'active', '2025-08-23 08:08:13', '2025-10-14 16:34:30');
INSERT INTO `products` VALUES (10, 'Claude_3.5_转发 API 全模型', 19.00, 0, 'https://ext.same-assets.com/754627011/1746394397.png', 1, '19元 / 10万', 'API密钥', 'api.claude.com', 'active', '2025-08-23 08:08:13', '2025-10-15 19:58:19');

-- ----------------------------
-- Table structure for stock_records
-- ----------------------------
DROP TABLE IF EXISTS `stock_records`;
CREATE TABLE `stock_records`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `product_id` int(0) NOT NULL,
  `order_id` int(0) NULL DEFAULT NULL,
  `change_type` enum('increase','decrease') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` int(0) NOT NULL,
  `before_stock` int(0) NOT NULL,
  `after_stock` int(0) NOT NULL,
  `reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '变更原因',
  `created_at` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  INDEX `order_id`(`order_id`) USING BTREE,
  CONSTRAINT `stock_records_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `stock_records_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
