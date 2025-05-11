from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

load_dotenv()  # Isso carrega as variáveis do .env automaticamente

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as err:
        print(f"Erro na conexão com o banco de dados: {err}")
        return None