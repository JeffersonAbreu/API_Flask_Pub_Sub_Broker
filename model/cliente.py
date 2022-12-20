from sqlalchemy import Column, Integer, String
from .base import Base
# Declaracao da classe


class Cliente(Base):

    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

    def __repr__(self):
        return f"Cliente {self.nome}"

    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco

    def toJSON(self):
        return {"id": self.id, "nome": self.nome, "endereco": self.endereco}