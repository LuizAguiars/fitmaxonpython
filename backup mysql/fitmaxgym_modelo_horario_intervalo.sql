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
-- Table structure for table `modelo_horario_intervalo`
--

DROP TABLE IF EXISTS `modelo_horario_intervalo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modelo_horario_intervalo` (
  `ID_Intervalo` int NOT NULL AUTO_INCREMENT,
  `ID_Modelo` int NOT NULL,
  `Dia_Semana` enum('Segunda','Terca','Quarta','Quinta','Sexta','Sabado','Domingo') NOT NULL,
  `Hora_Inicio` time NOT NULL,
  `Hora_Fim` time NOT NULL,
  PRIMARY KEY (`ID_Intervalo`),
  KEY `ID_Modelo` (`ID_Modelo`),
  CONSTRAINT `modelo_horario_intervalo_ibfk_1` FOREIGN KEY (`ID_Modelo`) REFERENCES `modelo_horario` (`ID_Modelo`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modelo_horario_intervalo`
--

LOCK TABLES `modelo_horario_intervalo` WRITE;
/*!40000 ALTER TABLE `modelo_horario_intervalo` DISABLE KEYS */;
INSERT INTO `modelo_horario_intervalo` VALUES (1,1,'Segunda','06:00:00','13:00:00'),(2,1,'Terca','06:00:00','13:00:00'),(3,1,'Quarta','06:00:00','13:00:00'),(4,1,'Quinta','06:00:00','13:00:00'),(5,1,'Sexta','06:00:00','13:00:00'),(6,1,'Sabado','06:00:00','13:00:00'),(7,1,'Domingo','06:00:00','13:00:00'),(8,2,'Segunda','14:00:00','22:00:00'),(9,2,'Terca','14:00:00','22:00:00'),(10,2,'Quarta','14:00:00','22:00:00'),(11,2,'Quinta','14:00:00','22:00:00'),(12,2,'Sexta','14:00:00','22:00:00'),(13,2,'Sabado','14:00:00','22:00:00'),(14,2,'Domingo','14:00:00','22:00:00'),(15,3,'Segunda','06:00:00','11:00:00'),(16,3,'Segunda','12:00:00','18:00:00'),(17,3,'Terca','06:00:00','11:00:00'),(18,3,'Terca','12:00:00','18:00:00'),(19,3,'Quarta','06:00:00','11:00:00'),(20,3,'Quarta','12:00:00','18:00:00'),(21,3,'Quinta','06:00:00','11:00:00'),(22,3,'Quinta','12:00:00','18:00:00'),(23,3,'Sexta','06:00:00','11:00:00'),(24,3,'Sexta','12:00:00','18:00:00'),(25,4,'Segunda','06:00:00','11:00:00'),(26,4,'Segunda','12:00:00','18:00:00'),(27,4,'Terca','06:00:00','11:00:00'),(28,4,'Terca','12:00:00','18:00:00'),(29,4,'Quarta','06:00:00','11:00:00'),(30,4,'Quarta','12:00:00','18:00:00'),(31,4,'Quinta','06:00:00','11:00:00'),(32,4,'Quinta','12:00:00','18:00:00'),(33,4,'Sexta','06:00:00','11:00:00'),(34,4,'Sexta','12:00:00','18:00:00'),(35,5,'Segunda','17:00:00','23:59:00'),(36,5,'Terca','17:00:00','23:59:00'),(37,5,'Quarta','17:00:00','23:59:00'),(38,5,'Quinta','17:00:00','23:59:00'),(39,5,'Sexta','17:00:00','23:59:00'),(40,6,'Segunda','06:00:00','12:00:00'),(41,6,'Terca','06:00:00','12:00:00'),(42,6,'Quarta','06:00:00','12:00:00'),(43,6,'Quinta','06:00:00','12:00:00'),(44,6,'Sexta','06:00:00','12:00:00');
/*!40000 ALTER TABLE `modelo_horario_intervalo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-19 15:53:24
