-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: test_database
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
-- Table structure for table `pepitos`
--

DROP TABLE IF EXISTS `pepitos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pepitos` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `flavour` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pepitos`
--

LOCK TABLES `pepitos` WRITE;
/*!40000 ALTER TABLE `pepitos` DISABLE KEYS */;
INSERT INTO `pepitos` VALUES (1,'Sweet'),(2,'UltraSweet'),(3,'Salty');
/*!40000 ALTER TABLE `pepitos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pepitos_purchases`
--

DROP TABLE IF EXISTS `pepitos_purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pepitos_purchases` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `pepito_id` int(10) unsigned NOT NULL,
  `credit_card_used` varchar(16) NOT NULL,
  `total_ammount` decimal(7,2) DEFAULT NULL,
  `purchased_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `userPepitoPurchase_idx` (`user_id`),
  KEY `pepitoPepitoPurchase_idx` (`pepito_id`),
  CONSTRAINT `pepitoPepitoPurchase` FOREIGN KEY (`pepito_id`) REFERENCES `pepitos` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `userPepitoPurchase` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pepitos_purchases`
--

LOCK TABLES `pepitos_purchases` WRITE;
/*!40000 ALTER TABLE `pepitos_purchases` DISABLE KEYS */;
INSERT INTO `pepitos_purchases` VALUES (1,1,1,'1111222233334444',10.00,'2025-03-27 03:01:09'),(2,1,3,'1111222233334444',15.00,'2025-03-27 03:01:09'),(3,2,2,'222333444555666',8.00,'2025-03-27 03:01:09'),(4,2,1,'222333444555666',15.00,'2025-03-27 03:01:09');
/*!40000 ALTER TABLE `pepitos_purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `user_email` varchar(150) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'jdoe','jon@doe.com','Jon','Doe','2025-03-27 02:58:32'),(2,'apearson','a@person.com','Austin','Pearson','2025-03-27 02:58:32');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'test_database'
--

--
-- Dumping routines for database 'test_database'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-27  0:05:03
