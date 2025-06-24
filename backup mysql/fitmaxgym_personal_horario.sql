-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: fitmaxgym
-- ------------------------------------------------------
-- Server version	9.3.0

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
-- Table structure for table `personal_horario`
--

DROP TABLE IF EXISTS `personal_horario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personal_horario` (
  `ID_Horario` int NOT NULL AUTO_INCREMENT,
  `ID_Personal` int NOT NULL,
  `Dia_Semana` enum('Segunda','Terca','Quarta','Quinta','Sexta','Sabado','Domingo') DEFAULT NULL,
  `Hora_Inicio` time NOT NULL,
  `Hora_Fim` time NOT NULL,
  `Ativo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`ID_Horario`),
  KEY `ID_Personal` (`ID_Personal`),
  CONSTRAINT `personal_horario_ibfk_1` FOREIGN KEY (`ID_Personal`) REFERENCES `personal` (`ID_Personal`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal_horario`
--

LOCK TABLES `personal_horario` WRITE;
/*!40000 ALTER TABLE `personal_horario` DISABLE KEYS */;
INSERT INTO `personal_horario` VALUES (1,5,'Segunda','07:00:00','12:00:00',1),(2,5,'Segunda','13:00:00','18:00:00',1),(3,5,'Terca','07:00:00','12:00:00',1),(4,5,'Terca','13:00:00','18:00:00',1),(5,5,'Quarta','07:00:00','12:00:00',1),(6,5,'Quarta','13:00:00','18:00:00',1),(7,5,'Quinta','07:00:00','12:00:00',1),(8,5,'Quinta','13:00:00','18:00:00',1),(9,5,'Sexta','07:00:00','12:00:00',1),(10,5,'Sexta','13:00:00','18:00:00',1),(16,6,'Segunda','17:00:00','23:59:00',1),(17,6,'Terca','17:00:00','23:59:00',1),(18,6,'Quarta','17:00:00','23:59:00',1),(19,6,'Quinta','17:00:00','23:59:00',1),(20,6,'Sexta','17:00:00','23:59:00',1),(21,7,'Segunda','17:00:00','23:59:00',1),(22,7,'Terca','17:00:00','23:59:00',1),(23,7,'Quarta','17:00:00','23:59:00',1),(24,7,'Quinta','17:00:00','23:59:00',1),(25,7,'Sexta','17:00:00','23:59:00',1),(26,8,'Segunda','17:00:00','23:59:00',1),(27,8,'Terca','17:00:00','23:59:00',1),(28,8,'Quarta','17:00:00','23:59:00',1),(29,8,'Quinta','17:00:00','23:59:00',1),(30,8,'Sexta','17:00:00','23:59:00',1),(31,9,'Segunda','06:00:00','12:00:00',1),(32,9,'Terca','06:00:00','12:00:00',1),(33,9,'Quarta','06:00:00','12:00:00',1),(34,9,'Quinta','06:00:00','12:00:00',1),(35,9,'Sexta','06:00:00','12:00:00',1);
/*!40000 ALTER TABLE `personal_horario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-19 15:53:26
