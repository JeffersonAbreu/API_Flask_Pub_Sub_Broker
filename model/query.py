# coding=utf-8
from .base import session_factory
from .cliente import Cliente
from .item_venda import ItemVenda
from .produto import Produto
from .venda import Venda
from sqlalchemy import *


class Query:
    def __init__(self):
        self.session = session_factory()
    # venda
    def vendaSave(self, id_cliente, tipo_pag, itens):
        total = 0
        for i in itens:
            total += i["preco"] * i["qtd"]
        venda = Venda(id_cliente, tipo_pag, total)
        for i in itens:
            item_venda = ItemVenda(i['produto_id'], i['qtd'], i['preco'], venda)
            self.session.add(item_venda)
        self.session.commit()
        return self.venda_UltimoID3()

    
    def venda_UltimoID(self) -> int:
        return self.session.query(Venda).order_by(Venda.id.desc()).first().id

    def venda_UltimoID2(self) -> int:
        return self.session.query(Venda).filter(Venda.id == self.session.query(func.max(Venda.id))).one().id
    
    def venda_UltimoID3(self) -> int:
        return self.session.execute('SELECT MAX(id) as id FROM venda').one().id

    def vendaUpdateStatus(self, id, status):
        self.session.query(Venda).filter(Venda.id == id).update(status)
        self.session.commit()

    def vendaByID(self, id: int) -> Venda:
        return self.session.query(Venda).filter(Venda.id == id).one()

    def vendaDelete(self, id):
        self.session.query(Venda).filter(Venda.id == id).delete()
        self.session.commit()

    def vendaAll(self) -> Venda:
        vendas_query = self.session.query(Venda)
        return vendas_query.all()

    # produto
    def produtoSave(self, produto):
        self.session.add(Produto(produto["nome"], produto["preco"]))
        self.session.commit()

    def produtoByID(self, id):
        return self.session.query(Produto).filter(Produto.id == id).one()

    def produtoUpdate(self, id, produto):
        self.session.query(Produto).filter(Produto.id == id).update(
            {
                "nome": produto["nome"],
                "preco": produto["preco"]
            }
        )
        self.session.commit()

    def produtoDelete(self, id):
        self.session.query(Produto).filter(Produto.id == id).delete()
        self.session.commit()

    def produtoAll(self):
        produtos_query = self.session.query(Produto)
        return produtos_query.all()

    # cliente
    def clienteSave(self, cliente):
        self.session.add(Cliente(cliente["nome"], cliente["endereco"]))
        self.session.commit()

    def clienteByID(self, id):
        return self.session.query(Cliente).filter(Cliente.id == id).one()

    def clienteUpdate(self, id, cliente):
        self.session.query(Cliente).filter(Cliente.id == id).update(
            {
                "nome": cliente["nome"],
                "endereco": cliente["endereco"]
            }
        )
        self.session.commit()

    def clienteDelete(self, id):
        self.session.query(Cliente).filter(Cliente.id == id).delete()
        self.session.commit()

    def clienteAll(self):
        clientes_query = self.session.query(Cliente)
        return clientes_query.all()
