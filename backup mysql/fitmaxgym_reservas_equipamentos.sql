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
-- Table structure for table `reservas_equipamentos`
--

DROP TABLE IF EXISTS `reservas_equipamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservas_equipamentos` (
  `idRESERVAS_EQUIPAMENTOS` int NOT NULL AUTO_INCREMENT,
  `ID_user` int DEFAULT NULL,
  `data_reserva` datetime NOT NULL,
  `id_equipamento` int DEFAULT NULL,
  `id_unidade_da_reserva` int DEFAULT NULL,
  `id_treino_agendado` int DEFAULT NULL,
  PRIMARY KEY (`idRESERVAS_EQUIPAMENTOS`),
  KEY `ID_user` (`ID_user`),
  KEY `id_equipamento` (`id_equipamento`),
  KEY `id_unidade_da_reserva` (`id_unidade_da_reserva`),
  KEY `id_treino_agendado` (`id_treino_agendado`),
  CONSTRAINT `reservas_equipamentos_ibfk_1` FOREIGN KEY (`ID_user`) REFERENCES `usuario` (`ID_User`),
  CONSTRAINT `reservas_equipamentos_ibfk_2` FOREIGN KEY (`id_equipamento`) REFERENCES `equipamentos` (`ID_equipamentos`),
  CONSTRAINT `reservas_equipamentos_ibfk_3` FOREIGN KEY (`id_unidade_da_reserva`) REFERENCES `unidades` (`ID_Unidades`),
  CONSTRAINT `reservas_equipamentos_ibfk_4` FOREIGN KEY (`id_treino_agendado`) REFERENCES `agendar_treino` (`idAgendar_Treino`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservas_equipamentos`
--

LOCK TABLES `reservas_equipamentos` WRITE;
/*!40000 ALTER TABLE `reservas_equipamentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `reservas_equipamentos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-27  1:49:47
