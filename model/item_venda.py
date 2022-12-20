# coding=utf-8

from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class ItemVenda(Base):
    __tablename__ = 'item_venda'

    id = Column(Integer, primary_key=True)
    qtd = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    produto_id = Column(Integer, ForeignKey("produto.id"))
    venda_id = Column(Integer, ForeignKey('venda.id', ondelete="CASCADE"))
    venda = relationship("Venda", back_populates="itens")

    def __init__(self, produto_id, qtd, preco, venda):
        self.produto_id = produto_id
        self.qtd = qtd
        self.preco = preco
        self.venda = venda

    def __repr__(self) -> str:
        return f"Item {self.id}"

    def toJSON(self):
        return {"id": self.id, "produto_id": self.produto_id, "qtd": self.qtd, "preco": self.preco}
