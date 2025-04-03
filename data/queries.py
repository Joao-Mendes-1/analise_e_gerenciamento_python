from sqlalchemy.orm import Session
from sqlalchemy import text

def get_clientes(db: Session):
    """ Retorna os clientes cadastrados no banco """
    query = text("SELECT id, nome, perfil_risco FROM clientes;")
    result = db.execute(query)
    return result.fetchall()

def get_transacoes(db: Session, cliente_id: int):
    """ Retorna o histórico de transações de um cliente específico """
    query = text("SELECT * FROM transacoes WHERE cliente_id = :cliente_id;")
    result = db.execute(query, {"cliente_id": cliente_id})
    return result.fetchall()
