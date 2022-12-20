from sqlalchemy import Column, Integer, String, Float
from .base import Base
# Declaracao da classe

class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"Produto {self.nome}"

    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def toJSON(self):
        return {"id": self.id, "nome": self.nome, "preco": self.preco}