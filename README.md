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
- MySQL  
- HTML + CSS (Jinja2)  
- JavaScript  
- Git + GitHub  

---

## ▶️ Como executar o projeto localmente

**1. Clone o repositório:**

```bash
git clone https://github.com/LuizAguiars/fitmaxonpython.git

2. Acesse a pasta do projeto:
cd fitmaxonpython


3. Crie um ambiente virtual (recomendado):
python -m venv venv

4. Ative o ambiente virtual:

No Windows:
venv\Scripts\activate

No Linux/Mac:
source venv/bin/activate

5. Instale as dependências do projeto:
pip install -r requirements.txt


6. Configure o banco de dados MySQL:
Crie o banco de dados com base nos arquivos .sql da pasta querys bd/

Atualize os dados de conexão no arquivo:

python app/app.py <--- para rodar o projeto


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


👤 Autor
Luiz Felipe Aguiar de Souza
Desenvolvedor de sistemas e estudante de Análise e Desenvolvimento de Sistemas.