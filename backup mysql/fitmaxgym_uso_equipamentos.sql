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
-- Table structure for table `uso_equipamentos`
--

DROP TABLE IF EXISTS `uso_equipamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uso_equipamentos` (
  `id_uso` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_equipamento` int NOT NULL,
  `id_treino_agendado` int NOT NULL,
  `data_uso` datetime DEFAULT CURRENT_TIMESTAMP,
  `tempo_utilizado_minutos` int NOT NULL,
  PRIMARY KEY (`id_uso`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_equipamento` (`id_equipamento`),
  KEY `id_treino_agendado` (`id_treino_agendado`),
  CONSTRAINT `uso_equipamentos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`ID_User`),
  CONSTRAINT `uso_equipamentos_ibfk_2` FOREIGN KEY (`id_equipamento`) REFERENCES `equipamentos` (`ID_equipamentos`),
  CONSTRAINT `uso_equipamentos_ibfk_3` FOREIGN KEY (`id_treino_agendado`) REFERENCES `agendar_treino` (`idAgendar_Treino`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uso_equipamentos`
--

LOCK TABLES `uso_equipamentos` WRITE;
/*!40000 ALTER TABLE `uso_equipamentos` DISABLE KEYS */;
INSERT INTO `uso_equipamentos` VALUES (8,1,1,2,'2025-05-27 01:05:51',10),(9,1,2,2,'2025-05-27 01:05:51',10),(10,1,1,3,'2025-05-27 01:06:10',10),(11,1,2,3,'2025-05-27 01:06:10',10),(12,1,3,3,'2025-05-27 01:06:10',10),(13,1,4,3,'2025-05-27 01:06:10',10),(14,1,1,5,'2025-05-27 01:14:38',10),(15,1,2,5,'2025-05-27 01:14:38',10),(16,1,3,5,'2025-05-27 01:14:38',10),(17,1,4,5,'2025-05-27 01:14:38',10),(18,1,1,6,'2025-05-27 01:18:30',10),(19,1,2,6,'2025-05-27 01:18:30',10),(20,1,3,6,'2025-05-27 01:18:30',10),(21,1,4,6,'2025-05-27 01:18:30',10),(22,1,1,7,'2025-05-27 01:22:54',10),(23,1,3,7,'2025-05-27 01:22:54',10),(24,1,1,10,'2025-05-27 18:05:49',20),(25,1,2,10,'2025-05-27 18:05:49',20),(26,1,3,10,'2025-05-27 18:05:49',20),(27,1,4,10,'2025-05-27 18:05:49',20),(28,1,1,18,'2025-05-28 17:55:27',10),(29,1,2,18,'2025-05-28 17:55:27',10),(30,1,1,11,'2025-05-28 20:43:32',60),(31,1,4,11,'2025-05-28 20:43:32',60),(32,4,1,12,'2025-05-28 20:43:36',60),(33,4,2,12,'2025-05-28 20:43:36',60),(34,4,3,12,'2025-05-28 20:43:36',60),(35,1,2,25,'2025-05-28 20:43:49',20);
/*!40000 ALTER TABLE `uso_equipamentos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-28 21:56:39
