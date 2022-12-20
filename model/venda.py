# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from .base import Base

class Venda(Base):
    __tablename__ = 'venda'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id", ondelete="CASCADE"))
    status = Column(String, nullable=False)
    tipo_pag = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    itens = relationship("ItemVenda", back_populates="venda", passive_deletes=True)

    def __init__(self, cliente_id, tipo_pag, total):
        self.cliente_id = cliente_id
        self.tipo_pag = tipo_pag
        self.status = "AGUARDANDO PAGAMENTO"
        self.total = total

    def toJSON(self):
        itens = []
        for i in self.itens:
            itens.append(i.toJSON())
        
        venda = {}
        venda['id']         = self.id
        venda["cliente_id"] = self.cliente_id
        venda['tipo_pag']   = self.tipo_pag
        venda["status"]     = self.status
        venda["total"]      = self.total
        venda["itens"]      = itens
        return venda