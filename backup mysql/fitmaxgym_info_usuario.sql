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
-- Table structure for table `info_usuario`
--

DROP TABLE IF EXISTS `info_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `info_usuario` (
  `ID_Info` int NOT NULL AUTO_INCREMENT,
  `ID_User` int NOT NULL,
  `Altura` decimal(4,2) DEFAULT NULL,
  `Peso` decimal(5,2) DEFAULT NULL,
  `GorduraCorporal` decimal(5,2) DEFAULT NULL,
  `Perimetro_Braquial` decimal(5,2) DEFAULT NULL,
  `Perimetro_Abdominal` decimal(5,2) DEFAULT NULL,
  `Perimetro_Toracico` decimal(5,2) DEFAULT NULL,
  `Perimetro_Cintura` decimal(5,2) DEFAULT NULL,
  `Perimetro_Quadril` decimal(5,2) DEFAULT NULL,
  `IMC` decimal(5,2) DEFAULT NULL,
  `DataMedicao` datetime DEFAULT CURRENT_TIMESTAMP,
  `Observacoes` text,
  `ClassificacaoGordura` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Info`),
  KEY `ID_User` (`ID_User`),
  CONSTRAINT `info_usuario_ibfk_1` FOREIGN KEY (`ID_User`) REFERENCES `usuario` (`ID_User`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_usuario`
--

LOCK TABLES `info_usuario` WRITE;
/*!40000 ALTER TABLE `info_usuario` DISABLE KEYS */;
INSERT INTO `info_usuario` VALUES (1,1,1.65,75.00,80.00,20.00,80.00,80.00,80.00,80.00,27.55,'2025-06-04 21:21:33','medidas de teste',NULL),(2,1,1.65,65.00,80.00,20.00,95.00,100.00,30.00,80.00,23.88,'2025-06-04 21:33:22','Teste 2',NULL),(3,1,1.65,50.00,50.00,39.00,80.00,80.00,60.00,30.00,18.37,'2025-06-04 21:39:18','Teste 3',NULL),(4,1,1.80,100.00,50.00,30.00,40.00,80.00,50.00,90.00,30.86,'2025-06-05 17:41:07',NULL,NULL),(5,1,1.65,80.00,60.00,20.00,80.00,80.00,90.00,80.00,29.38,'2025-06-06 16:50:34','Teste',NULL),(6,1,1.65,80.00,40.00,20.00,50.00,60.00,80.00,90.00,29.38,'2025-06-06 16:53:26','Teste2','Alto / Obesidade'),(7,1,1.65,80.00,20.00,20.00,90.00,80.00,80.00,90.00,29.38,'2025-06-06 16:55:48',NULL,'Normal'),(8,1,1.65,80.00,20.00,30.00,80.00,80.00,80.00,80.00,29.38,'2025-06-06 17:01:33',NULL,'Normal'),(9,1,1.65,80.00,20.00,30.00,80.00,80.00,80.00,80.00,29.38,'2025-06-06 17:01:33',NULL,'Normal'),(10,1,1.65,80.00,30.00,20.00,80.00,80.00,85.00,85.00,29.38,'2025-06-06 17:09:21','1','Alto / Obesidade'),(11,1,1.65,80.00,30.00,20.00,80.00,80.00,85.00,85.00,29.38,'2025-06-06 17:09:21','1','Alto / Obesidade'),(12,9,1.80,80.00,30.00,40.00,80.00,80.00,80.00,80.00,24.69,'2025-06-11 19:48:25','Teste','Alto / Obesidade'),(13,9,1.80,80.00,30.00,40.00,80.00,80.00,80.00,80.00,24.69,'2025-06-11 19:48:25','Teste','Alto / Obesidade');
/*!40000 ALTER TABLE `info_usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-11 22:20:24
