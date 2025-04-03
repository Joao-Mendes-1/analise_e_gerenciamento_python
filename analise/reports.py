import sys
import os
from sqlalchemy.orm import joinedload
from data.database import get_db
from data.models import Cliente, Transacao, Investimento
import pandas as pd

# Adiciona a pasta superior ao sys.path para que o config.py possa ser encontrado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def get_transacoes_cliente(db, cliente_id):
    """ Busca as transações de um cliente específico """
    return db.query(Transacao).filter(Transacao.cliente_id == cliente_id).all()

def get_investimentos_transacoes(db, transacoes):
    """ Busca os investimentos relacionados a cada transação """
    investimentos = {}
    for transacao in transacoes:
        investimento = db.query(Investimento).filter(Investimento.id == transacao.investimento_id).first()
        investimentos[transacao.id] = investimento.tipo_investimento if investimento else "Desconhecido"
    return investimentos

def gerar_relatorio(cliente, transacoes, investimentos):
    """ Gera um relatório em Excel do cliente """
    if not transacoes:
        print(f"Nenhuma transação encontrada para {cliente.nome_cliente}.")
        return

    # Converter objetos para dicionário antes de criar o DataFrame
    data = [
        {
            "Cliente": cliente.nome_cliente,
            "Data da Transação": t.data_transacao,
            "Valor": t.valor,
            "Tipo de Transação": t.tipo_transacao,
            "Tipo de Investimento": investimentos.get(t.id, "Desconhecido"),
        }
        for t in transacoes
    ]
    df = pd.DataFrame(data)

    # Nome do arquivo
    nome_arquivo = f"relatorio_{cliente.nome_cliente.replace(' ', '_')}.xlsx"
    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)

    df.to_excel(caminho_arquivo, index=False)
    print(f"Relatório gerado: {caminho_arquivo}")

def gerar_relatorio_todos_os_clientes(db):
    """ Gera um único relatório consolidado com todos os clientes e suas transações """
    clientes = db.query(Cliente).all()
    if not clientes:
        print("Nenhum cliente encontrado.")
        return

    dados = []
    for cliente in clientes:
        transacoes = get_transacoes_cliente(db, cliente.id)
        investimentos = get_investimentos_transacoes(db, transacoes)

        for t in transacoes:
            dados.append({
                "Cliente": cliente.nome_cliente,
                "Data da Transação": t.data_transacao,
                "Valor": t.valor,
                "Tipo de Transação": t.tipo_transacao,
                "Tipo de Investimento": investimentos.get(t.id, "Desconhecido"),
            })

    if not dados:
        print("Nenhuma transação encontrada para os clientes.")
        return

    df = pd.DataFrame(dados)

    # Nome do arquivo consolidado
    nome_arquivo = "relatorio_todos_clientes.xlsx"
    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)

    df.to_excel(caminho_arquivo, index=False)
    print(f"Relatório consolidado gerado: {caminho_arquivo}")

def main():
    db = next(get_db())

    # Gerar relatório de um único cliente
    cliente_id = 3  # Substitua pelo ID real do cliente
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    if cliente:
        transacoes = get_transacoes_cliente(db, cliente_id)
        investimentos = get_investimentos_transacoes(db, transacoes)
        gerar_relatorio(cliente, transacoes, investimentos)
    else:
        print(f"Cliente com ID {cliente_id} não encontrado.")

    # Gerar relatório para todos os clientes
    gerar_relatorio_todos_os_clientes(db)

if __name__ == "__main__":
    main()

