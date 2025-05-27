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
  `Data_Cadastro_user` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Data_Nascimento` date DEFAULT NULL,
  `Unidade_Prox_ID` int DEFAULT NULL,
  `cpf_user` varchar(14) NOT NULL,
  `endereco_user` varchar(100) DEFAULT NULL,
  `CEP_USER` varchar(10) DEFAULT NULL,
  `ID_PLANO` int DEFAULT NULL,
  `sexo_user` char(1) NOT NULL,
  `status_cliente` varchar(15) DEFAULT NULL,
  `pagou_mes_atual` tinyint(1) DEFAULT '0',
  `Tipo` tinyint NOT NULL DEFAULT '0',
  `telefone_user` varchar(20) DEFAULT NULL,
  `logradouro_user` varchar(100) DEFAULT NULL,
  `numero_user` varchar(10) DEFAULT NULL,
  `bairro_user` varchar(50) DEFAULT NULL,
  `cidade_user` varchar(50) DEFAULT NULL,
  `estado_user` char(2) DEFAULT NULL,
  PRIMARY KEY (`ID_User`),
  UNIQUE KEY `Email_user` (`Email_user`),
  UNIQUE KEY `cpf_user` (`cpf_user`),
  KEY `Unidade_Prox_ID` (`Unidade_Prox_ID`),
  KEY `ID_PLANO` (`ID_PLANO`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`Unidade_Prox_ID`) REFERENCES `unidades` (`ID_Unidades`),
  CONSTRAINT `usuario_ibfk_2` FOREIGN KEY (`ID_PLANO`) REFERENCES `plano` (`ID_PLANO`),
  CONSTRAINT `usuario_chk_1` CHECK ((`sexo_user` in (_utf8mb4'M',_utf8mb4'F',_utf8mb4'O'))),
  CONSTRAINT `usuario_chk_2` CHECK ((`status_cliente` in (_utf8mb4'Ativo',_utf8mb4'Inativo',_utf8mb4'Inadimplente'))),
  CONSTRAINT `usuario_chk_3` CHECK ((`Tipo` in (0,1,2)))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Luiz Felipe Aguiar de Souza','felipeonlinex@gmail.com','Luiz8474','1998-12-28 00:00:00','1998-12-28',5,'10907746993','Rua Cascavel','83410-270',2,'M','Ativo',1,0,'(41) 99999-9999','Cascavel','1221','Guaraituba','Colombo','PR'),(4,'Juliane Freitas dos Santos','julianefreitasst@gmail.com','1','2025-05-10 23:34:08','2000-01-17',5,'12427269930','Rua Castro','83410-270',1,'F','Ativo',0,0,'(41) 777777-7777','Castro','987','Guaraituba','Colombo','PR'),(5,'Luiz Felipe aguiar de souza','felipeonlinex1@gmail.com','1','2025-05-16 17:22:49','1998-12-28',NULL,'109.077.469-93',NULL,'83410-270',1,'M','Ativo',0,0,NULL,'Rua Cascavel','1221','Guaraituba','Colombo','PR'),(6,'Adilson Pereira','adilson@gmail.com','1','2025-05-16 17:43:51','2006-11-16',5,'019.750.669-01',NULL,'81070-190',1,'M','Ativo',0,0,'(11) 11111-1111','Rua Itajubá','673','Portão','Curitiba','PR'),(7,'Luiz Gustavo','luizgustavo@gmail.com','1','2025-05-16 19:43:55','2019-11-16',NULL,'117.152.019-06',NULL,'81020-010',2,'M','Ativo',0,0,'(41) 99999-9999','Avenida Brasília','5560','Novo Mundo','Curitiba','PR'),(8,'Teste user','teste@gmail.com','1','2025-05-16 21:53:23','2015-06-16',NULL,'128.726.729-74',NULL,'81070-090',1,'M','Ativo',0,0,'(41) 99999-9999','Rua Frei Gaspar da Madre de Deus','-10  ','Portão','Curitiba','PR');
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

-- Dump completed on 2025-05-26 22:27:11
