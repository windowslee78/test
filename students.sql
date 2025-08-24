-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        8.0.42 - MySQL Community Server - GPL
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 导出 students 的数据库结构
DROP DATABASE IF EXISTS `students`;
CREATE DATABASE IF NOT EXISTS `students` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `students`;

-- 导出  表 students.tb_admininfo 结构
DROP TABLE IF EXISTS `tb_admininfo`;
CREATE TABLE IF NOT EXISTS `tb_admininfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account` varchar(50) DEFAULT NULL COMMENT '帐号名',
  `password` varchar(50) DEFAULT NULL COMMENT '密码',
  `level` int DEFAULT NULL COMMENT '级别',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='管理员表';

-- 数据导出被取消选择。

-- 导出  表 students.tb_courseinfo 结构
DROP TABLE IF EXISTS `tb_courseinfo`;
CREATE TABLE IF NOT EXISTS `tb_courseinfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `coursename` varchar(50) DEFAULT NULL,
  `teacher` varchar(50) DEFAULT NULL COMMENT '教师',
  `score` int DEFAULT NULL COMMENT '学分',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课程信息表';

-- 数据导出被取消选择。

-- 导出  表 students.tb_studentsinfo 结构
DROP TABLE IF EXISTS `tb_studentsinfo`;
CREATE TABLE IF NOT EXISTS `tb_studentsinfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `number` varchar(50) NOT NULL COMMENT '学号，也是学生账号',
  `password` varchar(50) DEFAULT NULL COMMENT '学生密码',
  `name` varchar(10) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `other` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 数据导出被取消选择。

-- 导出  表 students.tb_student_course 结构
DROP TABLE IF EXISTS `tb_student_course`;
CREATE TABLE IF NOT EXISTS `tb_student_course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `courseid` int NOT NULL,
  `studentid` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学生选课信息表';

-- 数据导出被取消选择。

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
