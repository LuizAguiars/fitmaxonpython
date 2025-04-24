USE fitmaxgym;

-- REGIÃO
CREATE TABLE REGIAO (
    ID_Regiao INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Regiao VARCHAR(50) NOT NULL
);

-- UNIDADES
CREATE TABLE UNIDADES (
    ID_Unidades INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Unidade VARCHAR(100),
    Endereco_Unidade VARCHAR(255),
    ID_Regiao INT,
    Capacidade INT,
    fone INT,
    Cidade VARCHAR(100),
    Estado VARCHAR(100),
    CEP VARCHAR,

    FOREIGN KEY (ID_Regiao) REFERENCES REGIAO(ID_Regiao)
);

-- PLANOS
CREATE TABLE `plano` (
   `ID_PLANO` int NOT NULL AUTO_INCREMENT,
   `nome_plano` varchar(100) NOT NULL,
   `descricao` varchar(255) DEFAULT NULL,
   `duracao_meses` int NOT NULL,
   `valor_plano` decimal(10,2) NOT NULL,
   PRIMARY KEY (`ID_PLANO`)
 );

-- TIPO DE EQUIPAMENTO
CREATE TABLE tipo_equipamento (
    idtipo_equipamento INT AUTO_INCREMENT PRIMARY KEY,
    nome_tipo_equipamento VARCHAR(50) NOT NULL
);

-- STATUS DOS EQUIPAMENTOS
CREATE TABLE status_dos_Equipamentos (
    idstatus_dos_Equipamentos INT AUTO_INCREMENT PRIMARY KEY,
    status_do_Equipamento VARCHAR(50) NOT NULL
);

-- USUÁRIOS (CLIENTES)
CREATE TABLE USUARIO (
    ID_User INT AUTO_INCREMENT PRIMARY KEY,
    Nome_User VARCHAR(100) NOT NULL,
    Email_user VARCHAR(115) UNIQUE NOT NULL,
    Senha_User VARCHAR(255) NOT NULL,
    Data_Cadastro_user DATE NOT NULL,
    Unidade_Prox_ID INT,
    cpf_user VARCHAR(14) UNIQUE NOT NULL,
    endereco_user VARCHAR(100),
    CEP_USER VARCHAR(10),
    ID_PLANO INT,
    sexo_user CHAR(1) NOT NULL CHECK(sexo_user IN ('M', 'F', 'O')),
    status_cliente VARCHAR(15) CHECK(status_cliente IN ('Ativo', 'Inativo', 'Inadimplente')),
    pagou_mes_atual TINYINT(1) DEFAULT 0,
    FOREIGN KEY (Unidade_Prox_ID) REFERENCES UNIDADES(ID_Unidades),
    FOREIGN KEY (ID_PLANO) REFERENCES PLANO(ID_PLANO)
);

-- PERSONAL TRAINER
CREATE TABLE PERSONAL (
    ID_Personal INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Personal VARCHAR(100),
    Email_Personal VARCHAR(115) UNIQUE NOT NULL,
    Especialidade VARCHAR(100),
    ID_Unidade INT,
    FOREIGN KEY (ID_Unidade) REFERENCES UNIDADES(ID_Unidades)
);

-- EQUIPAMENTOS
CREATE TABLE EQUIPAMENTOS (
    ID_equipamentos INT AUTO_INCREMENT PRIMARY KEY,
    descricao_equipamentos VARCHAR(45) NOT NULL,
    data_de_compra DATETIME,
    ID_unidade_equipamento INT,
    Nome_Equipamento VARCHAR(45),
    id_status_do_equipamento INT,
    idtipo_equipamento INT,
    FOREIGN KEY (ID_unidade_equipamento) REFERENCES UNIDADES(ID_Unidades),
    FOREIGN KEY (id_status_do_equipamento) REFERENCES status_dos_Equipamentos(idstatus_dos_Equipamentos),
    FOREIGN KEY (idtipo_equipamento) REFERENCES tipo_equipamento(idtipo_equipamento)
);

-- TIPO DE TREINO
CREATE TABLE tipo_de_treino (
    idtipo_de_treino INT AUTO_INCREMENT PRIMARY KEY,
    nome_tipo_treino VARCHAR(100),
    descricao VARCHAR(255)
);

-- AGENDAMENTO DE TREINO
CREATE TABLE Agendar_Treino (
    idAgendar_Treino INT AUTO_INCREMENT PRIMARY KEY,
    ID_usuario INT,
    ID_Tipodetreino INT,
    ID_Personal INT,
    DataTreino DATE NOT NULL,
    HoraTreino TIME NOT NULL,
    ID_Unidade_Treino INT,
    FOREIGN KEY (ID_usuario) REFERENCES USUARIO(ID_User),
    FOREIGN KEY (ID_Tipodetreino) REFERENCES tipo_de_treino(idtipo_de_treino),
    FOREIGN KEY (ID_Unidade_Treino) REFERENCES UNIDADES(ID_Unidades),
    FOREIGN KEY (ID_Personal) REFERENCES PERSONAL(ID_Personal)
);

-- RESERVAS DE EQUIPAMENTO
CREATE TABLE RESERVAS_EQUIPAMENTOS (
    idRESERVAS_EQUIPAMENTOS INT AUTO_INCREMENT PRIMARY KEY,
    ID_user INT,
    data_reserva DATETIME NOT NULL,
    id_equipamento INT,
    id_unidade_da_reserva INT,
    id_treino_agendado INT,
    FOREIGN KEY (ID_user) REFERENCES USUARIO(ID_User),
    FOREIGN KEY (id_equipamento) REFERENCES EQUIPAMENTOS(ID_equipamentos),
    FOREIGN KEY (id_unidade_da_reserva) REFERENCES UNIDADES(ID_Unidades),
    FOREIGN KEY (id_treino_agendado) REFERENCES Agendar_Treino(idAgendar_Treino)
);

-- FEEDBACK DOS USUÁRIOS
CREATE TABLE feedback (
    idfeedback INT AUTO_INCREMENT PRIMARY KEY,
    id_user_feedback INT,
    id_unidade INT,
    nota_user INT CHECK(nota_user BETWEEN 1 AND 10),
    Comentario VARCHAR(600),
    FOREIGN KEY (id_user_feedback) REFERENCES USUARIO(ID_User),
    FOREIGN KEY (id_unidade) REFERENCES UNIDADES(ID_Unidades)
);

-- NOTIFICAÇÕES
CREATE TABLE notificacoes (
    idnotificacao INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    mensagem TEXT,
    data_envio DATETIME,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(ID_User)
);
