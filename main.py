from data.database import get_db
from data.models import Cliente, Investimento, Transacao
from sqlalchemy.orm import Session

def create_cliente(db: Session, nome: str, email: str, perfil_risco: str):
    db_cliente = Cliente(nome_cliente=nome, email_cliente=email, perfil_risco=perfil_risco)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def create_investimento(db: Session, cliente_id: int, tipo: str, valor: float, data_inicio):
    db_investimento = Investimento(cliente_id=cliente_id, tipo_investimento=tipo, valor_investido=valor, data_inicio=data_inicio)
    db.add(db_investimento)
    db.commit()
    db.refresh(db_investimento)
    return db_investimento

def create_transacao(db: Session, cliente_id: int, investimento_id: int, tipo_transacao: str, valor: float, data_transacao):
    db_transacao = Transacao(cliente_id=cliente_id, investimento_id=investimento_id, tipo_transacao=tipo_transacao, valor=valor, data_transacao=data_transacao)
    db.add(db_transacao)
    db.commit()
    db.refresh(db_transacao)
    return db_transacao

def main():
    db = next(get_db())
    
    # Criando clientes
    cliente1 = create_cliente(db, "João Mendes", "joao.mendes@email.com", "Moderado")
    cliente2 = create_cliente(db, "Maria Souza", "maria.souza@email.com", "Conservador")
    cliente3 = create_cliente(db, "Carlos Silva", "carlos.silva@email.com", "Agressivo")
    cliente4 = create_cliente(db, "Ana Oliveira", "ana.oliveira@email.com", "Moderado")

    # Criando investimentos para os clientes
    investimento1 = create_investimento(db, cliente1.id, "Ações", 10000.00, "2025-01-01")
    investimento2 = create_investimento(db, cliente2.id, "Tesouro Direto", 5000.00, "2025-01-10")
    investimento3 = create_investimento(db, cliente3.id, "Fundos Imobiliários", 15000.00, "2025-02-01")
    investimento4 = create_investimento(db, cliente4.id, "Criptomoedas", 20000.00, "2025-03-01")

    # Criando transações para os clientes
    transacao1 = create_transacao(db, cliente1.id, investimento1.id, "compra", 5000.00, "2025-01-01 10:00:00")
    transacao2 = create_transacao(db, cliente2.id, investimento2.id, "venda", 3000.00, "2025-01-15 15:00:00")
    transacao3 = create_transacao(db, cliente3.id, investimento3.id, "compra", 8000.00, "2025-02-10 09:00:00")
    transacao4 = create_transacao(db, cliente4.id, investimento4.id, "compra", 10000.00, "2025-03-05 12:00:00")

    # Imprimindo confirmação
    print(f"Cliente {cliente1.nome_cliente} com investimento de {investimento1.tipo_investimento} criado!")
    print(f"Cliente {cliente2.nome_cliente} com investimento de {investimento2.tipo_investimento} criado!")
    print(f"Cliente {cliente3.nome_cliente} com investimento de {investimento3.tipo_investimento} criado!")
    print(f"Cliente {cliente4.nome_cliente} com investimento de {investimento4.tipo_investimento} criado!")

if __name__ == "__main__":
    main()
