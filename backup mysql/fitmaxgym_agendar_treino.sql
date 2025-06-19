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
) ENGINE=InnoDB AUTO_INCREMENT=1129 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agendar_treino`
--

LOCK TABLES `agendar_treino` WRITE;
/*!40000 ALTER TABLE `agendar_treino` DISABLE KEYS */;
INSERT INTO `agendar_treino` VALUES (1,NULL,1,2,'2025-05-27','06:25:00',0,NULL,'Agendado',0),(2,1,1,2,'2025-05-27','00:35:00',0,5,'Concluído',0),(3,1,1,2,'2025-05-27','00:44:00',0,5,'Concluído',0),(4,1,1,3,'2025-05-27','04:45:00',0,5,'Cancelado',0),(5,1,1,2,'2025-05-27','01:12:00',0,5,'Concluído',0),(6,1,1,2,'2025-05-27','01:18:00',0,5,'Concluído',0),(7,1,1,2,'2025-05-27','01:22:00',0,5,'Concluído',0),(8,1,1,2,'2025-05-27','06:32:00',0,5,'Cancelado',0),(9,1,2,2,'2025-05-27','00:00:00',0,5,'Ausente',0),(10,1,2,2,'2025-05-27','07:01:00',0,5,'Concluído',0),(11,1,4,5,'2025-05-27','20:39:00',240,5,'Concluído',0),(12,4,4,5,'2025-05-27','21:12:00',240,5,'Concluído',0),(13,4,1,5,'2025-05-28','01:13:00',40,5,'Cancelado',0),(14,4,1,5,'2025-05-28','01:54:00',40,5,'Cancelado',0),(15,4,1,6,'2025-05-28','01:24:00',40,5,'Cancelado',0),(16,4,1,6,'2025-05-28','01:23:00',40,5,'Concluído',0),(17,1,1,6,'2025-05-27','21:47:00',40,5,'Concluído',1),(18,1,1,7,'2025-05-27','22:02:00',40,5,'Concluído',1),(19,1,2,8,'2025-05-27','22:18:00',80,5,'Concluído',1),(20,1,1,9,'2025-05-27','22:40:00',40,5,'Concluído',1),(21,1,1,10,'2025-05-27','22:54:00',40,5,'Agendado',1),(22,1,2,11,'2025-05-27','22:59:00',80,5,'Agendado',1),(23,1,1,12,'2025-05-28','00:05:00',40,5,'Cancelado',0),(24,1,2,12,'2025-05-28','00:10:00',80,5,'Concluído',0),(25,1,2,5,'2025-05-28','17:24:00',80,5,'Concluído',1),(26,1,2,6,'2025-05-28','17:24:00',80,5,'Concluído',0),(27,1,2,9,'2025-05-28','17:25:00',80,5,'Ausente',0),(28,1,2,7,'2025-05-28','17:59:00',80,5,'Agendado',1),(29,9,2,7,'2025-05-28','20:50:00',80,5,'Cancelado',0),(30,1,1,5,'2025-05-29','19:00:00',40,5,'Cancelado',0),(31,1,1,5,'2025-05-29','19:41:00',40,5,'Cancelado',0),(32,1,1,7,'2025-06-06','18:33:00',40,5,'Cancelado',0),(33,1,2,7,'2025-05-30','21:34:00',80,5,'Cancelado',0),(34,1,2,9,'2025-05-31','21:35:00',80,5,'Cancelado',0),(1100,1,1,8,'2025-05-31','08:57:00',40,5,'Cancelado',0),(1101,1,3,5,'2025-06-05','21:14:00',120,5,'Cancelado',0),(1102,1,1,5,'2025-05-29','21:10:00',40,5,'Concluído',1),(1103,1,1,7,'2025-06-06','13:45:00',40,5,'Cancelado',0),(1104,1,2,5,'2025-05-30','15:57:00',80,5,'Concluído',0),(1105,1,1,5,'2025-05-30','18:08:00',40,5,'Cancelado',0),(1106,7,1,6,'2025-05-30','16:10:00',40,5,'Concluído',0),(1107,1,4,5,'2025-05-30','21:20:00',240,5,'Cancelado',0),(1108,1,2,5,'2025-05-30','22:45:00',80,5,'Cancelado',0),(1109,1,1,8,'2025-06-02','21:17:00',40,5,'Cancelado',0),(1110,1,1,5,'2025-05-30','20:36:00',40,5,'Concluído',0),(1111,1,1,5,'2025-05-30','19:32:00',40,5,'Concluído',1),(1112,6,1,8,'2025-05-30','19:12:00',40,5,'Concluído',0),(1113,411,1,12,'2025-05-30','20:38:00',40,5,'Concluído',0),(1114,1,1,7,'2025-05-30','21:32:00',40,5,'Agendado',0),(1115,4,1,7,'2025-06-03','21:18:00',40,5,'Cancelado',0),(1116,1,1,5,'2025-06-03','12:36:00',40,5,'Concluído',0),(1117,1,1,5,'2025-06-04','19:11:00',40,5,'Ausente',0),(1118,1,1,5,'2025-06-04','21:10:00',40,5,'Concluído',1),(1119,1,1,8,'2025-06-04','23:04:00',40,5,'Agendado',0),(1120,1,1,7,'2025-06-05','08:00:00',40,5,'Agendado',0),(1121,1,1,5,'2025-06-06','17:09:00',40,5,'Ausente',0),(1122,1,1,5,'2025-06-06','18:51:00',40,5,'Ausente',1),(1123,1,1,5,'2025-06-11','22:00:00',40,5,'Cancelado',1),(1124,9,1,5,'2025-06-11','20:45:00',40,5,'Agendado',1),(1125,9,1,5,'2025-06-11','06:00:00',40,5,'Agendado',0),(1126,9,1,5,'2025-06-13','06:00:00',40,5,'Agendado',0),(1127,9,1,5,'2025-06-12','06:00:00',40,5,'Agendado',0),(1128,1,1,5,'2025-06-16','07:00:00',40,5,'Cancelado',0);
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

-- Dump completed on 2025-06-19 15:53:25
