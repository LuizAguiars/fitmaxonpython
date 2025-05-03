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
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `ID_User` int NOT NULL AUTO_INCREMENT,
  `Nome_User` varchar(100) NOT NULL,
  `Email_user` varchar(115) NOT NULL,
  `Senha_User` varchar(255) NOT NULL,
  `Data_Cadastro_user` date NOT NULL,
  `Unidade_Prox_ID` int DEFAULT NULL,
  `cpf_user` varchar(14) NOT NULL,
  `endereco_user` varchar(100) DEFAULT NULL,
  `CEP_USER` varchar(10) DEFAULT NULL,
  `ID_PLANO` int DEFAULT NULL,
  `sexo_user` char(1) NOT NULL,
  `status_cliente` varchar(15) DEFAULT NULL,
  `pagou_mes_atual` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ID_User`),
  UNIQUE KEY `Email_user` (`Email_user`),
  UNIQUE KEY `cpf_user` (`cpf_user`),
  KEY `Unidade_Prox_ID` (`Unidade_Prox_ID`),
  KEY `ID_PLANO` (`ID_PLANO`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`Unidade_Prox_ID`) REFERENCES `unidades` (`ID_Unidades`),
  CONSTRAINT `usuario_ibfk_2` FOREIGN KEY (`ID_PLANO`) REFERENCES `plano` (`ID_PLANO`),
  CONSTRAINT `usuario_chk_1` CHECK ((`sexo_user` in (_utf8mb4'M',_utf8mb4'F',_utf8mb4'O'))),
  CONSTRAINT `usuario_chk_2` CHECK ((`status_cliente` in (_utf8mb4'Ativo',_utf8mb4'Inativo',_utf8mb4'Inadimplente')))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'LUIZ FELIPE AGUIAR DE SOUZA','felipeonlinex@gmail.com','Luiz8474','1998-12-28',NULL,'10907746993','Rua Cascavel, 1221, Guaraituba, Colombo','83410-270',1,'M','Inativo',0),(3,'Gabriel Lopes Santana','gabriel.lopes@gmail.com','1234','2025-04-25',5,'8888888','Franssico Tissot, 900','987654321',2,'M','Ativo',1);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-03 15:07:30
