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
-- Table structure for table `equipamentos_por_tipo_treino`
--

DROP TABLE IF EXISTS `equipamentos_por_tipo_treino`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipamentos_por_tipo_treino` (
  `id_equipamento_tipo_treino` int NOT NULL AUTO_INCREMENT,
  `idtipo_de_treino` int NOT NULL,
  `id_equipamento` int NOT NULL,
  `tempo_minutos` int NOT NULL,
  PRIMARY KEY (`id_equipamento_tipo_treino`),
  KEY `idtipo_de_treino` (`idtipo_de_treino`),
  KEY `id_equipamento` (`id_equipamento`),
  CONSTRAINT `equipamentos_por_tipo_treino_ibfk_1` FOREIGN KEY (`idtipo_de_treino`) REFERENCES `tipo_de_treino` (`idtipo_de_treino`),
  CONSTRAINT `equipamentos_por_tipo_treino_ibfk_2` FOREIGN KEY (`id_equipamento`) REFERENCES `equipamentos` (`ID_equipamentos`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipamentos_por_tipo_treino`
--

LOCK TABLES `equipamentos_por_tipo_treino` WRITE;
/*!40000 ALTER TABLE `equipamentos_por_tipo_treino` DISABLE KEYS */;
INSERT INTO `equipamentos_por_tipo_treino` VALUES (1,1,1,10),(2,1,2,10),(3,1,3,10),(4,1,4,10),(5,2,1,20),(6,2,2,20),(7,2,3,20),(8,2,4,20),(9,3,1,30),(10,3,2,30),(11,3,4,30),(12,3,3,30),(13,4,1,60),(14,4,2,60),(15,4,3,60),(16,4,4,60),(17,5,1,60),(18,5,2,60),(19,5,3,60),(20,5,4,60);
/*!40000 ALTER TABLE `equipamentos_por_tipo_treino` ENABLE KEYS */;
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
