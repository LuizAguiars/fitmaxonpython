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
-- Table structure for table `agendar_treino`
--

DROP TABLE IF EXISTS `agendar_treino`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agendar_treino` (
  `idAgendar_Treino` int NOT NULL AUTO_INCREMENT,
  `ID_usuario` int DEFAULT NULL,
  `ID_Tipodetreino` int DEFAULT NULL,
  `ID_Personal` int DEFAULT NULL,
  `DataTreino` date NOT NULL,
  `HoraTreino` time NOT NULL,
  `DuracaoAula` int NOT NULL DEFAULT '0',
  `ID_Unidade_Treino` int DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Agendado',
  `notificado` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`idAgendar_Treino`),
  KEY `ID_usuario` (`ID_usuario`),
  KEY `ID_Tipodetreino` (`ID_Tipodetreino`),
  KEY `ID_Unidade_Treino` (`ID_Unidade_Treino`),
  KEY `ID_Personal` (`ID_Personal`),
  CONSTRAINT `agendar_treino_ibfk_1` FOREIGN KEY (`ID_usuario`) REFERENCES `usuario` (`ID_User`),
  CONSTRAINT `agendar_treino_ibfk_2` FOREIGN KEY (`ID_Tipodetreino`) REFERENCES `tipo_de_treino` (`idtipo_de_treino`),
  CONSTRAINT `agendar_treino_ibfk_3` FOREIGN KEY (`ID_Unidade_Treino`) REFERENCES `unidades` (`ID_Unidades`),
  CONSTRAINT `agendar_treino_ibfk_4` FOREIGN KEY (`ID_Personal`) REFERENCES `personal` (`ID_Personal`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agendar_treino`
--

LOCK TABLES `agendar_treino` WRITE;
/*!40000 ALTER TABLE `agendar_treino` DISABLE KEYS */;
INSERT INTO `agendar_treino` VALUES (1,NULL,1,2,'2025-05-27','06:25:00',0,NULL,'Agendado',0),(2,1,1,2,'2025-05-27','00:35:00',0,5,'Concluído',0),(3,1,1,2,'2025-05-27','00:44:00',0,5,'Concluído',0),(4,1,1,3,'2025-05-27','04:45:00',0,5,'Cancelado',0),(5,1,1,2,'2025-05-27','01:12:00',0,5,'Concluído',0),(6,1,1,2,'2025-05-27','01:18:00',0,5,'Concluído',0),(7,1,1,2,'2025-05-27','01:22:00',0,5,'Concluído',0),(8,1,1,2,'2025-05-27','06:32:00',0,5,'Cancelado',0),(9,1,2,2,'2025-05-27','00:00:00',0,5,'Ausente',0),(10,1,2,2,'2025-05-27','07:01:00',0,5,'Concluído',0),(11,1,4,5,'2025-05-27','20:39:00',240,5,'Agendado',0),(12,4,4,5,'2025-05-27','21:12:00',240,5,'Agendado',0),(13,4,1,5,'2025-05-28','01:13:00',40,5,'Cancelado',0),(14,4,1,5,'2025-05-28','01:54:00',40,5,'Cancelado',0),(15,4,1,6,'2025-05-28','01:24:00',40,5,'Cancelado',0),(16,4,1,6,'2025-05-28','01:23:00',40,5,'Agendado',0);
/*!40000 ALTER TABLE `agendar_treino` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-27 20:54:52
