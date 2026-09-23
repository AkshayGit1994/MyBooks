-- MySQL dump 10.13  Distrib 8.4.9, for Linux (x86_64)
--
-- Host: localhost    Database: Mybooks
-- ------------------------------------------------------
-- Server version	8.4.9

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `Mybooks`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Mybooks` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `Mybooks`;

--
-- Table structure for table `Authors`
--

DROP TABLE IF EXISTS `Authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Authors` (
  `AuthorId` int NOT NULL AUTO_INCREMENT,
  `AuthorName` varchar(20) NOT NULL,
  `Gender` varchar(6) NOT NULL,
  PRIMARY KEY (`AuthorId`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Authors`
--

LOCK TABLES `Authors` WRITE;
/*!40000 ALTER TABLE `Authors` DISABLE KEYS */;
INSERT INTO `Authors` VALUES (100,'Adrian Tchaikovsky','Male'),(101,'Alex Michaelides','Male'),(102,'Neil Gaiman','Male'),(103,'Douglas Adams','Male'),(104,'Andy Weir','Male'),(105,'Holly Black','Female'),(106,'John Sandford','Male'),(107,'Robert T. Kiyosaki','Male'),(108,'James Clear','Male'),(109,'Sarah J. Maas','Female');
/*!40000 ALTER TABLE `Authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Books`
--

DROP TABLE IF EXISTS `Books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Books` (
  `BookId` int NOT NULL AUTO_INCREMENT,
  `BookName` varchar(40) NOT NULL,
  `Year` year NOT NULL,
  `Genre` varchar(10) NOT NULL,
  `AuthorId` int NOT NULL,
  `Status` varchar(12) NOT NULL DEFAULT 'Finished',
  PRIMARY KEY (`BookId`),
  KEY `fk_books_authors` (`AuthorId`),
  CONSTRAINT `fk_books_authors` FOREIGN KEY (`AuthorId`) REFERENCES `Authors` (`AuthorId`)
) ENGINE=InnoDB AUTO_INCREMENT=1017 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Books`
--

LOCK TABLES `Books` WRITE;
/*!40000 ALTER TABLE `Books` DISABLE KEYS */;
INSERT INTO `Books` VALUES (1000,'Children of Time',2015,'Sci-Fi',100,'Finished'),(1001,'The Silent Patient',2019,'Thriller',101,'Finished'),(1002,'Coraline',2002,'Fantasy',102,'Finished'),(1003,'The Hitchhiker\'s Guide to the Galaxy',1979,'Sci-Fi',103,'Finished'),(1004,'Project Hail Mary',2021,'Sci-Fi',104,'Finished'),(1005,'The Cruel Prince',2018,'Fantasy',105,'Finished'),(1006,'Shroud',2026,'Sci-Fi',100,'Want to Read'),(1007,'Children of Ruin',2019,'Sci-Fi',100,'Want to Read'),(1008,'Children of Memory',2022,'Sci-Fi',100,'Want to Read'),(1009,'Children of Strife',2026,'Sci-Fi',100,'Want to Read'),(1010,'Saturn Run',2015,'Sci-Fi',106,'Cancelled'),(1011,'Rich Dad Poor Dad',1997,'Self-Help',107,'Finished'),(1012,'Atomic Habits',2018,'Self-Help',108,'Finished'),(1013,'Alien Clay',2024,'Sci-Fi',100,'Want to Read'),(1014,'The Assassin\'s Blade',2014,'Fantasy',109,'Cancelled'),(1015,'The Wicked King',2019,'Fantasy',105,'Reading'),(1016,'The Queen of Nothing',2019,'Fantasy',105,'Want to Read');
/*!40000 ALTER TABLE `Books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `Count`
--

DROP TABLE IF EXISTS `Count`;
/*!50001 DROP VIEW IF EXISTS `Count`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `Count` AS SELECT 
 1 AS `Status`,
 1 AS `Count`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `ReadStatus`
--

DROP TABLE IF EXISTS `ReadStatus`;
/*!50001 DROP VIEW IF EXISTS `ReadStatus`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `ReadStatus` AS SELECT 
 1 AS `BookName`,
 1 AS `Year`,
 1 AS `Genre`,
 1 AS `AuthorName`,
 1 AS `Status`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'Mybooks'
--

--
-- Current Database: `Mybooks`
--

USE `Mybooks`;

--
-- Final view structure for view `Count`
--

/*!50001 DROP VIEW IF EXISTS `Count`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`akshay`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `Count` AS select `Books`.`Status` AS `Status`,count(`Books`.`Status`) AS `Count` from `Books` group by `Books`.`Status` order by `Count` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `ReadStatus`
--

/*!50001 DROP VIEW IF EXISTS `ReadStatus`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`akshay`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `ReadStatus` AS select `B`.`BookName` AS `BookName`,`B`.`Year` AS `Year`,`B`.`Genre` AS `Genre`,`A`.`AuthorName` AS `AuthorName`,`B`.`Status` AS `Status` from (`Books` `B` join `Authors` `A` on((`B`.`AuthorId` = `A`.`AuthorId`))) order by `B`.`Status` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-23 19:54:37
