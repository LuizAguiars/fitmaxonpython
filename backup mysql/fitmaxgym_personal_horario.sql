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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal_horario`
--

LOCK TABLES `personal_horario` WRITE;
/*!40000 ALTER TABLE `personal_horario` DISABLE KEYS */;
INSERT INTO `personal_horario` VALUES (1,5,'Segunda','07:00:00','12:00:00',1),(2,5,'Segunda','13:00:00','18:00:00',1),(3,5,'Terca','07:00:00','12:00:00',1),(4,5,'Terca','13:00:00','18:00:00',1),(5,5,'Quarta','07:00:00','12:00:00',1),(6,5,'Quarta','13:00:00','18:00:00',1),(7,5,'Quinta','07:00:00','12:00:00',1),(8,5,'Quinta','13:00:00','18:00:00',1),(9,5,'Sexta','07:00:00','12:00:00',1),(10,5,'Sexta','13:00:00','18:00:00',1);
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

-- Dump completed on 2025-06-11 22:20:25
