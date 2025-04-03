from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Date, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_cliente = Column(String(255), nullable=False)
    email_cliente = Column(String(255))
    perfil_risco = Column(String(50))

    investimentos = relationship("Investimento", back_populates="cliente")
    transacoes = relationship("Transacao", back_populates="cliente")

class Investimento(Base):
    __tablename__ = 'investimentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    tipo_investimento = Column(String(255), nullable=False)
    valor_investido = Column(DECIMAL(10, 2))
    data_inicio = Column(Date)

    cliente = relationship("Cliente", back_populates="investimentos")
    transacoes = relationship("Transacao", back_populates="investimento")

class Transacao(Base):
    __tablename__ = 'transacoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    investimento_id = Column(Integer, ForeignKey('investimentos.id'))
    tipo_transacao = Column(String(50))
    valor = Column(DECIMAL(10, 2))
    data_transacao = Column(TIMESTAMP)

    cliente = relationship("Cliente", back_populates="transacoes")
    investimento = relationship("Investimento", back_populates="transacoes")
