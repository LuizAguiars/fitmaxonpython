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
-- Table structure for table `equipamentos`
--

DROP TABLE IF EXISTS `equipamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipamentos` (
  `ID_equipamentos` int NOT NULL AUTO_INCREMENT,
  `descricao_equipamentos` varchar(45) NOT NULL,
  `data_de_compra` datetime DEFAULT NULL,
  `ID_unidade_equipamento` int DEFAULT NULL,
  `Nome_Equipamento` varchar(45) DEFAULT NULL,
  `id_status_do_equipamento` int DEFAULT NULL,
  `idtipo_equipamento` int DEFAULT NULL,
  PRIMARY KEY (`ID_equipamentos`),
  KEY `ID_unidade_equipamento` (`ID_unidade_equipamento`),
  KEY `id_status_do_equipamento` (`id_status_do_equipamento`),
  KEY `idtipo_equipamento` (`idtipo_equipamento`),
  CONSTRAINT `equipamentos_ibfk_1` FOREIGN KEY (`ID_unidade_equipamento`) REFERENCES `unidades` (`ID_Unidades`),
  CONSTRAINT `equipamentos_ibfk_2` FOREIGN KEY (`id_status_do_equipamento`) REFERENCES `status_dos_equipamentos` (`idstatus_dos_Equipamentos`),
  CONSTRAINT `equipamentos_ibfk_3` FOREIGN KEY (`idtipo_equipamento`) REFERENCES `tipo_equipamento` (`idtipo_equipamento`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipamentos`
--

LOCK TABLES `equipamentos` WRITE;
/*!40000 ALTER TABLE `equipamentos` DISABLE KEYS */;
INSERT INTO `equipamentos` VALUES (1,'Esteira modelo 2929 ','2025-04-24 00:00:00',5,'Esteira',1,1),(2,'Bicicleta modelo 1010','2025-05-14 00:00:00',5,'Bicicleta Ergométrica',1,1),(3,'Modelo: 2025','2025-04-25 00:00:00',5,'Leg Press',1,2),(4,'modelo 2025','2025-04-25 00:00:00',5,'Supino',1,2);
/*!40000 ALTER TABLE `equipamentos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-05 18:00:37
