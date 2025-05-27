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
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `idfeedback` int NOT NULL AUTO_INCREMENT,
  `id_user_feedback` int DEFAULT NULL,
  `id_unidade` int DEFAULT NULL,
  `nota_user` int DEFAULT NULL,
  `Comentario` varchar(600) DEFAULT NULL,
  `Outro` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`idfeedback`),
  KEY `id_user_feedback` (`id_user_feedback`),
  KEY `id_unidade` (`id_unidade`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`id_user_feedback`) REFERENCES `usuario` (`ID_User`),
  CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`id_unidade`) REFERENCES `unidades` (`ID_Unidades`),
  CONSTRAINT `feedback_chk_1` CHECK ((`nota_user` between 1 and 10))
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,1,NULL,3,'teste',NULL),(2,1,NULL,1,'lgbt',NULL),(3,1,NULL,2,'teste',NULL),(7,1,NULL,5,'teste',NULL),(8,1,NULL,4,'amorim burro',NULL),(9,1,5,3,'Teste com comentários','Falta de limpeza, Pouca variedade de equipamentos'),(10,1,5,4,'amorim burro','Equipamentos em bom estado, Atendimento atencioso, Limpeza e organização'),(11,1,5,3,'gay','Equipamentos quebrados, Falta de limpeza, Atendimento ruim, Atrasos nas aulas, Pouca variedade de equipamentos, Ambiente barulhento'),(12,1,5,3,'Teste','Falta de limpeza, Atendimento ruim'),(13,1,5,1,'adasd','Atendimento ruim'),(14,1,5,5,'asdsada','Personal bem capacitado'),(15,1,5,3,'sadsad','Atrasos nas aulas'),(16,1,5,5,'sadasda',NULL),(17,1,5,5,'',NULL),(18,1,5,4,'',NULL),(19,1,5,5,'',NULL),(20,1,5,2,'',NULL),(21,1,5,4,'',NULL),(22,1,5,5,'',NULL),(23,1,5,1,'',NULL),(24,1,6,5,'aaa','Ambiente agradável'),(25,1,5,4,'aa',NULL),(26,1,5,5,'',NULL),(27,1,5,4,'',NULL),(28,1,7,4,'',NULL),(29,1,5,5,'',NULL),(30,1,6,3,'sadasd','Falta de limpeza'),(31,1,7,5,'',NULL),(32,1,5,1,'',NULL),(33,1,7,1,'',NULL),(34,1,7,5,'',NULL),(35,1,7,5,'',NULL),(36,1,7,3,'blz','Falta de limpeza, Atendimento ruim, Atrasos nas aulas');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
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
