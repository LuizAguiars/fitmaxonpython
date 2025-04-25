-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema fitmaxgym
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema fitmaxgym
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `fitmaxgym` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `fitmaxgym` ;

-- -----------------------------------------------------
-- Table `fitmaxgym`.`regiao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`regiao` (
  `ID_Regiao` INT NOT NULL AUTO_INCREMENT,
  `Nome_Regiao` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`ID_Regiao`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`unidades`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`unidades` (
  `ID_Unidades` INT NOT NULL AUTO_INCREMENT,
  `Nome_Unidade` VARCHAR(100) NULL DEFAULT NULL,
  `Endereco_Unidade` VARCHAR(255) NULL DEFAULT NULL,
  `ID_Regiao` INT NULL DEFAULT NULL,
  `Capacidade` INT NULL DEFAULT NULL,
  `Fone` VARCHAR(20) NULL DEFAULT NULL,
  `Cidade` VARCHAR(100) NULL DEFAULT NULL,
  `Estado` VARCHAR(100) NULL DEFAULT NULL,
  `CEP` VARCHAR(15) NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Unidades`),
  INDEX `ID_Regiao` (`ID_Regiao` ASC) VISIBLE,
  CONSTRAINT `unidades_ibfk_1`
    FOREIGN KEY (`ID_Regiao`)
    REFERENCES `fitmaxgym`.`regiao` (`ID_Regiao`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`plano`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`plano` (
  `ID_PLANO` INT NOT NULL AUTO_INCREMENT,
  `nome_plano` VARCHAR(100) NOT NULL,
  `descricao` VARCHAR(255) NULL DEFAULT NULL,
  `duracao_meses` INT NOT NULL,
  `valor_plano` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`ID_PLANO`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`usuario` (
  `ID_User` INT NOT NULL AUTO_INCREMENT,
  `Nome_User` VARCHAR(100) NOT NULL,
  `Email_user` VARCHAR(115) NOT NULL,
  `Senha_User` VARCHAR(255) NOT NULL,
  `Data_Cadastro_user` DATE NOT NULL,
  `Unidade_Prox_ID` INT NULL DEFAULT NULL,
  `cpf_user` VARCHAR(14) NOT NULL,
  `endereco_user` VARCHAR(100) NULL DEFAULT NULL,
  `CEP_USER` VARCHAR(10) NULL DEFAULT NULL,
  `ID_PLANO` INT NULL DEFAULT NULL,
  `sexo_user` CHAR(1) NOT NULL,
  `status_cliente` VARCHAR(15) NULL DEFAULT NULL,
  `pagou_mes_atual` TINYINT(1) NULL DEFAULT '0',
  PRIMARY KEY (`ID_User`),
  UNIQUE INDEX `Email_user` (`Email_user` ASC) VISIBLE,
  UNIQUE INDEX `cpf_user` (`cpf_user` ASC) VISIBLE,
  INDEX `Unidade_Prox_ID` (`Unidade_Prox_ID` ASC) VISIBLE,
  INDEX `ID_PLANO` (`ID_PLANO` ASC) VISIBLE,
  CONSTRAINT `usuario_ibfk_1`
    FOREIGN KEY (`Unidade_Prox_ID`)
    REFERENCES `fitmaxgym`.`unidades` (`ID_Unidades`),
  CONSTRAINT `usuario_ibfk_2`
    FOREIGN KEY (`ID_PLANO`)
    REFERENCES `fitmaxgym`.`plano` (`ID_PLANO`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`tipo_de_treino`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`tipo_de_treino` (
  `idtipo_de_treino` INT NOT NULL AUTO_INCREMENT,
  `nome_tipo_treino` VARCHAR(100) NULL DEFAULT NULL,
  `descricao` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`idtipo_de_treino`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`personal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`personal` (
  `ID_Personal` INT NOT NULL AUTO_INCREMENT,
  `Nome_Personal` VARCHAR(100) NULL DEFAULT NULL,
  `Email_Personal` VARCHAR(115) NOT NULL,
  `Especialidade` VARCHAR(100) NULL DEFAULT NULL,
  `ID_Unidade` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Personal`),
  UNIQUE INDEX `Email_Personal` (`Email_Personal` ASC) VISIBLE,
  INDEX `ID_Unidade` (`ID_Unidade` ASC) VISIBLE,
  CONSTRAINT `personal_ibfk_1`
    FOREIGN KEY (`ID_Unidade`)
    REFERENCES `fitmaxgym`.`unidades` (`ID_Unidades`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`agendar_treino`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`agendar_treino` (
  `idAgendar_Treino` INT NOT NULL AUTO_INCREMENT,
  `ID_usuario` INT NULL DEFAULT NULL,
  `ID_Tipodetreino` INT NULL DEFAULT NULL,
  `ID_Personal` INT NULL DEFAULT NULL,
  `DataTreino` DATE NOT NULL,
  `HoraTreino` TIME NOT NULL,
  `ID_Unidade_Treino` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idAgendar_Treino`),
  INDEX `ID_usuario` (`ID_usuario` ASC) VISIBLE,
  INDEX `ID_Tipodetreino` (`ID_Tipodetreino` ASC) VISIBLE,
  INDEX `ID_Unidade_Treino` (`ID_Unidade_Treino` ASC) VISIBLE,
  INDEX `ID_Personal` (`ID_Personal` ASC) VISIBLE,
  CONSTRAINT `agendar_treino_ibfk_1`
    FOREIGN KEY (`ID_usuario`)
    REFERENCES `fitmaxgym`.`usuario` (`ID_User`),
  CONSTRAINT `agendar_treino_ibfk_2`
    FOREIGN KEY (`ID_Tipodetreino`)
    REFERENCES `fitmaxgym`.`tipo_de_treino` (`idtipo_de_treino`),
  CONSTRAINT `agendar_treino_ibfk_3`
    FOREIGN KEY (`ID_Unidade_Treino`)
    REFERENCES `fitmaxgym`.`unidades` (`ID_Unidades`),
  CONSTRAINT `agendar_treino_ibfk_4`
    FOREIGN KEY (`ID_Personal`)
    REFERENCES `fitmaxgym`.`personal` (`ID_Personal`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`status_dos_equipamentos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`status_dos_equipamentos` (
  `idstatus_dos_Equipamentos` INT NOT NULL AUTO_INCREMENT,
  `status_do_Equipamento` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`idstatus_dos_Equipamentos`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`tipo_equipamento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`tipo_equipamento` (
  `idtipo_equipamento` INT NOT NULL AUTO_INCREMENT,
  `nome_tipo_equipamento` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`idtipo_equipamento`))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`equipamentos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`equipamentos` (
  `ID_equipamentos` INT NOT NULL AUTO_INCREMENT,
  `descricao_equipamentos` VARCHAR(45) NOT NULL,
  `data_de_compra` DATETIME NULL DEFAULT NULL,
  `ID_unidade_equipamento` INT NULL DEFAULT NULL,
  `Nome_Equipamento` VARCHAR(45) NULL DEFAULT NULL,
  `id_status_do_equipamento` INT NULL DEFAULT NULL,
  `idtipo_equipamento` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID_equipamentos`),
  INDEX `ID_unidade_equipamento` (`ID_unidade_equipamento` ASC) VISIBLE,
  INDEX `id_status_do_equipamento` (`id_status_do_equipamento` ASC) VISIBLE,
  INDEX `idtipo_equipamento` (`idtipo_equipamento` ASC) VISIBLE,
  CONSTRAINT `equipamentos_ibfk_1`
    FOREIGN KEY (`ID_unidade_equipamento`)
    REFERENCES `fitmaxgym`.`unidades` (`ID_Unidades`),
  CONSTRAINT `equipamentos_ibfk_2`
    FOREIGN KEY (`id_status_do_equipamento`)
    REFERENCES `fitmaxgym`.`status_dos_equipamentos` (`idstatus_dos_Equipamentos`),
  CONSTRAINT `equipamentos_ibfk_3`
    FOREIGN KEY (`idtipo_equipamento`)
    REFERENCES `fitmaxgym`.`tipo_equipamento` (`idtipo_equipamento`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`equipamentos_por_tipo_treino`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`equipamentos_por_tipo_treino` (
  `id_equipamento_tipo_treino` INT NOT NULL AUTO_INCREMENT,
  `idtipo_de_treino` INT NOT NULL,
  `id_equipamento` INT NOT NULL,
  `tempo_minutos` INT NOT NULL,
  PRIMARY KEY (`id_equipamento_tipo_treino`),
  INDEX `idtipo_de_treino` (`idtipo_de_treino` ASC) VISIBLE,
  INDEX `id_equipamento` (`id_equipamento` ASC) VISIBLE,
  CONSTRAINT `equipamentos_por_tipo_treino_ibfk_1`
    FOREIGN KEY (`idtipo_de_treino`)
    REFERENCES `fitmaxgym`.`tipo_de_treino` (`idtipo_de_treino`),
  CONSTRAINT `equipamentos_por_tipo_treino_ibfk_2`
    FOREIGN KEY (`id_equipamento`)
    REFERENCES `fitmaxgym`.`equipamentos` (`ID_equipamentos`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`feedback`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`feedback` (
  `idfeedback` INT NOT NULL AUTO_INCREMENT,
  `id_user_feedback` INT NULL DEFAULT NULL,
  `id_unidade` INT NULL DEFAULT NULL,
  `nota_user` INT NULL DEFAULT NULL,
  `Comentario` VARCHAR(600) NULL DEFAULT NULL,
  PRIMARY KEY (`idfeedback`),
  INDEX `id_user_feedback` (`id_user_feedback` ASC) VISIBLE,
  INDEX `id_unidade` (`id_unidade` ASC) VISIBLE,
  CONSTRAINT `feedback_ibfk_1`
    FOREIGN KEY (`id_user_feedback`)
    REFERENCES `fitmaxgym`.`usuario` (`ID_User`),
  CONSTRAINT `feedback_ibfk_2`
    FOREIGN KEY (`id_unidade`)
    REFERENCES `fitmaxgym`.`unidades` (`ID_Unidades`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`notificacoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`notificacoes` (
  `idnotificacao` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NULL DEFAULT NULL,
  `mensagem` TEXT NULL DEFAULT NULL,
  `data_envio` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`idnotificacao`),
  INDEX `id_usuario` (`id_usuario` ASC) VISIBLE,
  CONSTRAINT `notificacoes_ibfk_1`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `fitmaxgym`.`usuario` (`ID_User`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`reservas_equipamentos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`reservas_equipamentos` (
  `idRESERVAS_EQUIPAMENTOS` INT NOT NULL AUTO_INCREMENT,
  `ID_user` INT NULL DEFAULT NULL,
  `data_reserva` DATETIME NOT NULL,
  `id_equipamento` INT NULL DEFAULT NULL,
  `id_unidade_da_reserva` INT NULL DEFAULT NULL,
  `id_treino_agendado` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idRESERVAS_EQUIPAMENTOS`),
  INDEX `ID_user` (`ID_user` ASC) VISIBLE,
  INDEX `id_equipamento` (`id_equipamento` ASC) VISIBLE,
  INDEX `id_unidade_da_reserva` (`id_unidade_da_reserva` ASC) VISIBLE,
  INDEX `id_treino_agendado` (`id_treino_agendado` ASC) VISIBLE,
  CONSTRAINT `reservas_equipamentos_ibfk_1`
    FOREIGN KEY (`ID_user`)
    REFERENCES `fitmaxgym`.`usuario` (`ID_User`),
  CONSTRAINT `reservas_equipamentos_ibfk_2`
    FOREIGN KEY (`id_equipamento`)
    REFERENCES `fitmaxgym`.`equipamentos` (`ID_equipamentos`),
  CONSTRAINT `reservas_equipamentos_ibfk_3`
    FOREIGN KEY (`id_unidade_da_reserva`)
    REFERENCES `fitmaxgym`.`unidades` (`ID_Unidades`),
  CONSTRAINT `reservas_equipamentos_ibfk_4`
    FOREIGN KEY (`id_treino_agendado`)
    REFERENCES `fitmaxgym`.`agendar_treino` (`idAgendar_Treino`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fitmaxgym`.`uso_equipamentos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitmaxgym`.`uso_equipamentos` (
  `id_uso` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NOT NULL,
  `id_equipamento` INT NOT NULL,
  `id_treino_agendado` INT NOT NULL,
  `data_uso` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `tempo_utilizado_minutos` INT NOT NULL,
  PRIMARY KEY (`id_uso`),
  INDEX `id_usuario` (`id_usuario` ASC) VISIBLE,
  INDEX `id_equipamento` (`id_equipamento` ASC) VISIBLE,
  INDEX `id_treino_agendado` (`id_treino_agendado` ASC) VISIBLE,
  CONSTRAINT `uso_equipamentos_ibfk_1`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `fitmaxgym`.`usuario` (`ID_User`),
  CONSTRAINT `uso_equipamentos_ibfk_2`
    FOREIGN KEY (`id_equipamento`)
    REFERENCES `fitmaxgym`.`equipamentos` (`ID_equipamentos`),
  CONSTRAINT `uso_equipamentos_ibfk_3`
    FOREIGN KEY (`id_treino_agendado`)
    REFERENCES `fitmaxgym`.`agendar_treino` (`idAgendar_Treino`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
