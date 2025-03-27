-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: challengeml
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `control_affected_tags`
--

DROP TABLE IF EXISTS `control_affected_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `control_affected_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `control_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `affect_score_by` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `control_id` (`control_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `control_affected_tags_ibfk_1` FOREIGN KEY (`control_id`) REFERENCES `controls` (`id`),
  CONSTRAINT `control_affected_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `datatype_tags` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_affected_tags`
--

LOCK TABLES `control_affected_tags` WRITE;
/*!40000 ALTER TABLE `control_affected_tags` DISABLE KEYS */;
INSERT INTO `control_affected_tags` VALUES (1,1,1,80),(2,2,1,30),(3,3,1,10),(4,3,3,30),(5,3,5,30),(6,4,5,80),(7,5,3,80),(8,6,2,80),(9,7,4,80),(10,8,2,50);
/*!40000 ALTER TABLE `control_affected_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `controls`
--

DROP TABLE IF EXISTS `controls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `controls` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `raw_data` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by_id` (`created_by_id`),
  CONSTRAINT `controls_ibfk_1` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controls`
--

LOCK TABLES `controls` WRITE;
/*!40000 ALTER TABLE `controls` DISABLE KEYS */;
INSERT INTO `controls` VALUES (1,'RegExOnFieldName','Check for the literal string username',1,'2025-03-26 22:47:12','{\"regex\": \"username|USERNAME\"}'),(2,'RegExOnFieldName','Search for the string user',1,'2025-03-26 22:47:12','{\"regex\": \".*(user|USER).*\"}'),(3,'RegExOnFieldName','Search for the string name',1,'2025-03-26 22:47:12','{\"regex\": \".*(name|NAME).*\"}'),(4,'RegExOnFieldName','Search for common ways of reffering to the last_name',1,'2025-03-26 22:47:12','{\"regex\": \"(last|LAST|SUR|sur)(_|-)?(name|NAME)\"}'),(5,'RegExOnFieldName','Search for common ways of reffering to the first_name',1,'2025-03-26 22:47:12','{\"regex\": \"(first|FIRST)(_|-)?(name|NAME)\"}'),(6,'RegExOnFieldName','Search for various ways of naming an email field',1,'2025-03-26 22:47:12','{\"regex\": \".*(e|E)?(mail|MAIL)((_|-)?(address|ADDRESS))?\"}'),(7,'RegExOnFieldName','Search for various any pattern containing combinations of credit and card',1,'2025-03-26 22:47:12','{\"regex\": \".*(CREDIT|credit)(_|-)?(CARD|card).*\"}'),(8,'RegExOnSampledData','Email address pattern',1,'2025-03-26 22:47:12','{\"regex\": \"[^@]+@[^@]+\\\\.[^@]+\"}');
/*!40000 ALTER TABLE `controls` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `databases`
--

DROP TABLE IF EXISTS `databases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `databases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(10) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by_id` (`created_by_id`),
  CONSTRAINT `databases_ibfk_1` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `databases`
--

LOCK TABLES `databases` WRITE;
/*!40000 ALTER TABLE `databases` DISABLE KEYS */;
/*!40000 ALTER TABLE `databases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datatype_tags`
--

DROP TABLE IF EXISTS `datatype_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datatype_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `created_by_id` (`created_by_id`),
  CONSTRAINT `datatype_tags_ibfk_1` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datatype_tags`
--

LOCK TABLES `datatype_tags` WRITE;
/*!40000 ALTER TABLE `datatype_tags` DISABLE KEYS */;
INSERT INTO `datatype_tags` VALUES (1,'USERNAME','An username',1,'2025-03-26 22:47:12'),(2,'EMAIL_ADDRESS','An email address',1,'2025-03-26 22:47:12'),(3,'FIRST_NAME','A persons name',1,'2025-03-26 22:48:12'),(4,'CREDIT_CARD_NUMBER',NULL,1,'2025-03-26 22:47:12'),(5,'LAST_NAME','A persons last name',1,'2025-03-26 22:47:12');
/*!40000 ALTER TABLE `datatype_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `field_tags`
--

DROP TABLE IF EXISTS `field_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `field_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `certanty_score` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `field_id` (`field_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `field_tags_ibfk_1` FOREIGN KEY (`field_id`) REFERENCES `table_fields` (`id`),
  CONSTRAINT `field_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `datatype_tags` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `field_tags`
--

LOCK TABLES `field_tags` WRITE;
/*!40000 ALTER TABLE `field_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `field_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mysql_databases`
--

DROP TABLE IF EXISTS `mysql_databases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mysql_databases` (
  `id` int(11) NOT NULL,
  `host` text NOT NULL,
  `port` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `mysql_databases_ibfk_1` FOREIGN KEY (`id`) REFERENCES `databases` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mysql_databases`
--

LOCK TABLES `mysql_databases` WRITE;
/*!40000 ALTER TABLE `mysql_databases` DISABLE KEYS */;
/*!40000 ALTER TABLE `mysql_databases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scan_result`
--

DROP TABLE IF EXISTS `scan_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scan_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `executed_on` datetime NOT NULL,
  `database_id` int(11) NOT NULL,
  `requested_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `database_id` (`database_id`),
  KEY `requested_by_id` (`requested_by_id`),
  CONSTRAINT `scan_result_ibfk_1` FOREIGN KEY (`database_id`) REFERENCES `databases` (`id`),
  CONSTRAINT `scan_result_ibfk_2` FOREIGN KEY (`requested_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scan_result`
--

LOCK TABLES `scan_result` WRITE;
/*!40000 ALTER TABLE `scan_result` DISABLE KEYS */;
/*!40000 ALTER TABLE `scan_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schema_tables`
--

DROP TABLE IF EXISTS `schema_tables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schema_tables` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `schema_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `schema_id` (`schema_id`),
  CONSTRAINT `schema_tables_ibfk_1` FOREIGN KEY (`schema_id`) REFERENCES `schemas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schema_tables`
--

LOCK TABLES `schema_tables` WRITE;
/*!40000 ALTER TABLE `schema_tables` DISABLE KEYS */;
/*!40000 ALTER TABLE `schema_tables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schemas`
--

DROP TABLE IF EXISTS `schemas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schemas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `scan_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scan_id` (`scan_id`),
  CONSTRAINT `schemas_ibfk_1` FOREIGN KEY (`scan_id`) REFERENCES `scan_result` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schemas`
--

LOCK TABLES `schemas` WRITE;
/*!40000 ALTER TABLE `schemas` DISABLE KEYS */;
/*!40000 ALTER TABLE `schemas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `table_fields`
--

DROP TABLE IF EXISTS `table_fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_fields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `type` enum('STRING','INTEGER','DECIMAL','BOOLEAN','BINARY','TIME','DATE','DATETIME') NOT NULL,
  `table_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `table_id` (`table_id`),
  CONSTRAINT `table_fields_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `schema_tables` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `table_fields`
--

LOCK TABLES `table_fields` WRITE;
/*!40000 ALTER TABLE `table_fields` DISABLE KEYS */;
/*!40000 ALTER TABLE `table_fields` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `_password_hash` varchar(72) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'testAdmin','$2a$10$L87OOGIttHUz2t2AoGjElOuYOmm2TDUHcwvlIEi.JhGHO4toUeJ9i',1,'2025-03-26 23:37:00','2025-01-01 00:00:00'),(2,'testUser','$2a$10$34FheJEq1lwF8TDIRHUE9OeZwPtLKaBHCynFy2NCte9m.flUQ2odK',0,'2025-03-26 22:51:29','2025-01-01 00:00:00');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'challengeml'
--

--
-- Dumping routines for database 'challengeml'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-26 23:46:02
