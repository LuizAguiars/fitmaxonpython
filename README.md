🏋️‍♂️ Fitmax - Sistema de Gestão para Academia
Sistema desenvolvido em Python com Flask para controle e gerenciamento de academias, com foco em unidades, clientes, colaboradores e agendamentos. Ideal para o dia a dia administrativo da Fitmax.

📋 Funcionalidades principais
📦 Cadastro de clientes, funcionários e unidades

📅 Reserva de horários por unidade

🧾 Controle financeiro (sem pagamento online)

🔔 Sistema de notificações

📈 Geração de relatórios diversos

📋 Cadastro de equipamentos e controle de status

👤 Login com controle de acesso por perfil (gestor/personal)

🕒 Registro e controle de ponto dos funcionários

📊 Painéis de acompanhamento

⚙️ Tecnologias utilizadas
Python 3.11

Flask

MySQL Workbench e MySQL Server

HTML + CSS (Jinja2)

JavaScript

Git + GitHub

▶️ Como executar o projeto localmente
1. Clone o repositório
bash
Copiar
Editar
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@exemplo.com"

git clone https://github.com/LuizAguiars/fitmaxonpython.git
cd fitmaxonpython
2. Crie e ative o ambiente virtual
bash
Copiar
Editar
python -m venv venv
Ative o ambiente:

No Windows:

bash
Copiar
Editar
venv\Scripts\activate
No Linux/Mac:

bash
Copiar
Editar
source venv/bin/activate
3. Instale as dependências
bash
Copiar
Editar
pip install -r requirements.txt
Se ainda não funcionar, rode:

bash
Copiar
Editar
pip install flask
pip install mysql-connector-python
4. Configure o banco de dados MySQL
🔄 Importar Backup .sql via MySQL Workbench
Pré-requisitos:

MySQL Workbench instalado

Acesso ao servidor MySQL

Arquivo .sql localizado em:
C:\fitmaxcompleto\backup mysql\fitmax_backup.sql

📌 Etapas:
Abra o MySQL Workbench
Conecte-se à instância local do MySQL.

Crie o banco de dados:

sql
Copiar
Editar
CREATE DATABASE fitmaxgym;
Depois, no painel esquerdo (SCHEMAS), clique com o botão direito em fitmaxgym → Set as Default Schema.

Importe o backup:

Vá em: Server > Data Import

Selecione: Import from Self-Contained File

Em File path, selecione:

makefile
Copiar
Editar
C:\fitmaxcompleto\backup mysql\fitmax_backup.sql
Em Default Target Schema, selecione ou digite fitmaxgym

Clique em Start Import e aguarde aparecer "Import Completed"

Verifique se as tabelas foram importadas com sucesso

5. Verifique a conexão com o banco no backend
No arquivo app.py, a conexão está assim:

python
Copiar
Editar
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='8474',
        database='fitmaxgym'
    )
🔐 Ajuste a senha (password) conforme a senha do seu MySQL local.
Se estiver diferente, o sistema não irá funcionar.

6. Execute o sistema
bash
Copiar
Editar
python app/app.py
ou

bash
Copiar
Editar
python app.py
7. Acesse no navegador
arduino
Copiar
Editar
http://localhost:5000
📁 Estrutura de Pastas
csharp
Copiar
Editar
fitmaxonpython/
├── app/                 # Arquivos principais do sistema
├── comandos/            # Scripts auxiliares e documentação
├── querys bd/           # Scripts SQL de criação e insert
├── static/              # Arquivos estáticos (CSS, JS)
├── templates/           # Páginas HTML do sistema (Jinja2)
├── requirements.txt     # Lista de dependências do projeto
└── README.md            # Este arquivo