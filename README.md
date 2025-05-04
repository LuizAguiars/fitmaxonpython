# 🏋️‍♂️ Fitmax - Sistema de Gestão para Academia

Sistema desenvolvido em Python com Flask para controle e gerenciamento de academias, com foco em unidades, clientes, colaboradores e agendamentos. Ideal para o dia a dia administrativo da Fitmax.

---

## 📋 Funcionalidades principais

- 📦 Cadastro de clientes, funcionários e unidades  
- 📅 Reserva de horários por unidade  
- 🧾 Controle financeiro (sem pagamento online)  
- 🔔 Sistema de notificações  
- 📈 Geração de relatórios diversos  
- 📋 Cadastro de equipamentos e controle de status  
- 👤 Login com controle de acesso por perfil (gestor/personal)  
- 🕒 Registro e controle de ponto dos funcionários  
- 📊 Painéis de acompanhamento  

---

## ⚙️ Tecnologias utilizadas

- Python 3.11  
- Flask  
- MySQL Worchbench e MysqlServer
- HTML + CSS (Jinja2)  
- JavaScript  
- Git + GitHub  

---

## ▶️ Como executar o projeto localmente

**1. Clone o repositório:**


```bash

INSTRUÇÕES PARA CLONAR O PROJETO

1. Acesse a pasta do projeto:
cd fitmaxonpython

esses comandos é apenas para a PRIMEIRA CONFIGURAÇÃO do git
Configure o Git com seu usuário
Abra o terminal git bash na pasta onde deseja iniciar (clonar, baixar) o projeto e digite:

git config --global user.name "Seu Nome"
git config --global user.email "seuemail@exemplo.com"

✅ Esses dados serão usados nos commits então coloque as informações corretas.

Clone o repositório
no git bash dentro da pasta onde deseja clonar (baixar o projeto) digite:
git clone https://github.com/LuizAguiars/fitmaxonpython.git


3. Crie um ambiente virtual (recomendado):
python -m venv venv

4. Ative o ambiente virtual:

No Windows:
venv\Scripts\activate

No Linux/Mac:
source venv/bin/activate

5. Instale as dependências do projeto:
pip install -r requirements.txt

5.1. Atenção se o codigo não rodar após a instalação dos requirements.txt
execute os seguintes comandos
1: pip install flask
2: pip install mysql-connector-python


6. Configure o banco de dados MySQL:
🗂️ Importar Backup .sql usando Data Import no MySQL Workbench
🛠️ Pré-requisitos
MySQL Workbench instalado

Acesso ao seu servidor MySQL

Arquivo .sql localizado em:
C:pastadoprojeto-->\fitmaxcompleto\backup mysql\

✅ Passo a Passo
1. Abrir o MySQL Workbench
Inicie o programa

Conecte-se à instância MySQL (ex: Local instance MySQL)

2. Criar o banco de dados
Execute no editor:


3. Crie o banco de dados vazio

CREATE DATABASE fitmaxgym;
Depois:

No painel esquerdo (SCHEMAS), clique com o botão direito em fitmaxgym > Set as Default Schema

3. Acessar o menu Data Import
Vá em:
Server > Data Import

4. Selecionar o tipo de importação
Marque: Import from Self-Contained File

Em File path, clique em ... e selecione o seu arquivo, por exemplo:
C:\fitmaxcompleto\backup mysql\fitmax_backup.sql

5. Selecionar o banco de destino
Em Default Target Schema, selecione fitmaxgym
(Se não aparecer, clique em “New…” e digite fitmaxgym manualmente)

6. Executar a importação
Clique em Start Import

Aguarde até o processo completar (deve mostrar “Import Completed” no final)

7. Verificar
Vá até o painel esquerdo → fitmaxgym

Clique em Tables → verifique se as tabelas apareceram com os dados

⚠️ Observação Importante
No arquivo app.py (backend), a conexão com o banco de dados está definida da seguinte forma:

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='8474',
        database='fitmaxgym'
    )


Se a senha (password) configurada acima for diferente da senha do seu MySQL local, o sistema não conseguirá se conectar ao banco de dados.
🔐 Certifique-se de ajustar a senha conforme a sua instalação.




python app/app.py ou python app.py <--- para rodar o projeto



8. Acesse o sistema no navegador:
http://localhost:5000

📁 Estrutura de pastas
fitmaxonpython/
├── app/                 # Arquivos principais do sistema
├── comandos/            # Scripts auxiliares e documentação
├── querys bd/           # Scripts SQL de criação e insert
├── static/              # Arquivos estáticos (CSS, JS)
├── templates/           # Páginas HTML do sistema (Jinja2)
├── requirements.txt     # Lista de dependências do projeto
└── README.md            # Este arquivo

