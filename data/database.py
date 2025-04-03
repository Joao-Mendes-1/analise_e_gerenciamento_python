import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adiciona a pasta superior ao sys.path para que o config.py possa ser encontrado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config  # Agora importa o config.py que está na pasta superior

# URL do banco de dados usando as credenciais do config.py
DATABASE_URL = f"postgresql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}/{config.DB_NAME}"

# Criação da engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Criação do SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """ Retorna uma sessão do banco de dados """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Testando a conexão diretamente
try:
    # Conectando com o banco apenas para verificar se tudo está ok
    with engine.connect() as connection:
        print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro na conexão: {e}")
