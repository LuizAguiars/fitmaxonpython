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
-- Table structure for table `personal`
--

DROP TABLE IF EXISTS `personal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personal` (
  `ID_Personal` int NOT NULL AUTO_INCREMENT,
  `Nome_Personal` varchar(100) DEFAULT NULL,
  `Email_Personal` varchar(115) NOT NULL,
  `Especialidade` varchar(100) DEFAULT NULL,
  `ID_Unidade` int DEFAULT NULL,
  `Senha_Personal` varchar(100) NOT NULL DEFAULT '1',
  `DataNascimento` date DEFAULT NULL,
  `Telefone` varchar(20) DEFAULT NULL,
  `CPF` varchar(14) DEFAULT NULL,
  `Genero` enum('M','F','O') DEFAULT 'O',
  `Bio` text,
  `CertificadoNome` varchar(150) DEFAULT NULL,
  `CertificadoCodigo` varchar(50) DEFAULT NULL,
  `CertificadoEmissor` varchar(100) DEFAULT NULL,
  `CertificadoData` date DEFAULT NULL,
  `DataCadastro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID_Personal`),
  UNIQUE KEY `Email_Personal` (`Email_Personal`),
  KEY `ID_Unidade` (`ID_Unidade`),
  CONSTRAINT `personal_ibfk_1` FOREIGN KEY (`ID_Unidade`) REFERENCES `unidades` (`ID_Unidades`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal`
--

LOCK TABLES `personal` WRITE;
/*!40000 ALTER TABLE `personal` DISABLE KEYS */;
INSERT INTO `personal` VALUES (2,'Silvio Bortoleto','silviobortoleto@unicesumar.com','treinamento funcional',6,'1','1998-12-28','(41) 99999-9999','109.077.469-93','M',NULL,'Educação Fisica','KSJD9812Y7812DYH781H','CESUMAR CURITIBA','2025-06-11','2025-06-04 19:54:49'),(3,'Alexandre Bento','alexandre.bento@unicesumar.com','Musculação',7,'1',NULL,NULL,NULL,'O',NULL,NULL,NULL,NULL,NULL,'2025-06-04 19:54:49'),(5,'Luiz Fernando Corcini','luiz.corcini@unicesumar.edu.br','Musculação',5,'1',NULL,NULL,NULL,'O',NULL,NULL,NULL,NULL,NULL,'2025-06-04 19:54:49'),(6,'Paulo Gomes','paulogomes@gmail.com','treinamento funcional',5,'1',NULL,NULL,NULL,'O',NULL,NULL,NULL,NULL,NULL,'2025-06-04 19:54:49'),(7,'Adalberto Junior','Adalberto@fitmax.com.br','Musculação',5,'1',NULL,NULL,NULL,'O',NULL,NULL,NULL,NULL,NULL,'2025-06-04 19:54:49'),(8,'Gabriel Barbosa','gabriel@fitmax.com.br','Musculação',5,'1',NULL,NULL,NULL,'O',NULL,NULL,NULL,NULL,NULL,'2025-06-04 19:54:49'),(9,'Pedro Henrique','pedro.henrique@fitmax.com.br','Musculação',5,'1',NULL,NULL,NULL,'O',NULL,NULL,NULL,NULL,NULL,'2025-06-04 19:54:49'),(10,'Brian Santos','brian.santos@fitmax.com.br','Musculação',5,'1',NULL,NULL,NULL,'O',NULL,NULL,NULL,NULL,NULL,'2025-06-04 19:54:49'),(11,'Caique Santos','caique.santos@fitmax.com.br','treinamento funcional',5,'1',NULL,NULL,NULL,'O',NULL,NULL,NULL,NULL,NULL,'2025-06-04 19:54:49'),(12,'Welington Souza','welington.souza@fitmax.com.br','treinamento de atletas de alta performance',5,'1',NULL,NULL,NULL,'O',NULL,NULL,NULL,NULL,NULL,'2025-06-04 19:54:49'),(13,'Willian Cardoso','contato.fitmax.cwb@gmail.com','treinamento funcional',6,'1','2005-01-04','(41) 99999-9999','109.077.469-93','M',NULL,'Educação Fisica','SAJDHY1279TY12DG126GD1','CESUMAR CURITIBA','2003-01-05','2025-06-04 20:10:24'),(16,'Silvia Cardoso','contrato.fitmax@gmail.com','treinamento de atletas de alta performance',6,'1','2005-02-04','(41) 9999-9999','109.077.469-93','F',NULL,'Educação Fisica','SAJDHQ2178H1281278H182','UFPR','1998-05-08','2025-06-04 20:25:18'),(18,'Teste Fitmax','fitmax@gmail.com','Musculação',6,'1','1998-12-28','(41) 99999-9999','109.077.469-93','M',NULL,'Educação Fisica','ADJBQUWDB1N2D238472','UFPR','2025-06-06','2025-06-06 16:40:07');
/*!40000 ALTER TABLE `personal` ENABLE KEYS */;
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
