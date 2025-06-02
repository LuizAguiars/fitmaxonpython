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
-- Table structure for table `unidades`
--

DROP TABLE IF EXISTS `unidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidades` (
  `ID_Unidades` int NOT NULL AUTO_INCREMENT,
  `Nome_Unidade` varchar(100) DEFAULT NULL,
  `Capacidade` int DEFAULT NULL,
  `Fone` varchar(20) DEFAULT NULL,
  `logradouro_unidade` varchar(100) DEFAULT NULL,
  `numero_unidade` varchar(10) DEFAULT NULL,
  `bairro_unidade` varchar(50) DEFAULT NULL,
  `cidade_unidade` varchar(50) DEFAULT NULL,
  `estado_unidade` char(2) DEFAULT NULL,
  `cep_unidade` varchar(10) DEFAULT NULL,
  `CNPJ` varchar(18) DEFAULT NULL,
  `Email` varchar(120) DEFAULT NULL,
  `Horario_Funcionamento_ID` int DEFAULT NULL,
  `Ativa` tinyint(1) DEFAULT '1',
  `Data_Cadastro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID_Unidades`),
  KEY `fk_horario_funcionamento` (`Horario_Funcionamento_ID`),
  CONSTRAINT `fk_horario_funcionamento` FOREIGN KEY (`Horario_Funcionamento_ID`) REFERENCES `horarios_funcionamento` (`ID_Horario`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades`
--

LOCK TABLES `unidades` WRITE;
/*!40000 ALTER TABLE `unidades` DISABLE KEYS */;
INSERT INTO `unidades` VALUES (5,'Unidade  Guaraituba',100,'(41) 98760-9987','Rua Cascavel','1221','Guaraituba','Colombo','PR','83410-270','65.857.639/0001-01','fitmax.guaraituba@fitmax.com.br',1,1,'2025-05-28 19:45:30'),(6,'Unidade Portão',100,'(41) 98788-8888','Rua Itajubá','3789','Portão','Curitiba','PR','81070-190','65.857.639/0001-02','fitmax.portao@fitmax.com.br',1,1,'2025-05-28 19:45:30'),(7,'Unidade Cabral',100,'(41) 99878-8874','Avenida Cândido de Abreu','589','Centro Cívico','Curitiba','PR','80530-908','65.857.639/0001-03','fitmax.portao@fitmax.com.br',1,1,'2025-05-28 19:45:30'),(9,'Unidade Pinhais',100,'(41) 3666-0008','Rua Senegal','432','Pineville','Pinhais','PR','83320-090','65.857.639/0001-04','fitmax.pinhas@fitmax.com.br',1,1,'2025-05-29 20:14:07'),(10,'Unidade São José dos Pinhais',100,'(41) 3666-0202','Rua das Acácias','529','Costeira','São José dos Pinhais','PR','83015-390','65.857.639/0001-05','fitmax.pinhais@fitmax.com.br',1,1,'2025-05-29 20:39:48'),(11,'Unidade Almirante Tamandaré',100,'(41) 3666-0404','Rua Alice de Siqueira','2981','Colônia Antônio Prado','Almirante Tamandaré','PR','83502-120','65.857.639/0001-06','tamandare@fitmax.com.br',1,1,'2025-05-29 20:58:05');
/*!40000 ALTER TABLE `unidades` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 23:08:16
