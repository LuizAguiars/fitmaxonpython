INSERT INTO REGIAO (Nome_Regiao)
VALUES 
    ('Norte'),
    ('Sul'),
    ('Leste'),
    ('Oeste');

ALTER TABLE PLANO
ADD COLUMN valor_plano DECIMAL(10,2) NOT NULL;

INSERT INTO PLANO (nome_plano, descricao, duracao_meses, valor_plano)
VALUES 
    ('Medio', 'Plano intermediário com acesso limitado a recursos premium', 1, 79.90),
    ('Full', 'Plano completo com todos os recursos disponíveis', 6, 100.00);

ALTER TABLE USUARIO
ADD COLUMN Senha_User VARCHAR(255) NOT NULL;





INSERT INTO tipo_equipamento (nome_tipo_equipamento) VALUES
('Equipamentos de Cardio'),
('Equipamentos de Musculação'),
('Equipamentos Funcionais'),
('Equipamentos de Alongamento'),
('Equipamentos de Pilates'),
('Equipamentos de Artes Marciais'),
('Acessórios Livres');


INSERT INTO status_dos_Equipamentos (status_do_Equipamento) VALUES
('Ativo'),
('Inativo'),
('Manutenção'),
('Descartado');

