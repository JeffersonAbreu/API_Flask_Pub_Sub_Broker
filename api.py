from flask import Flask, jsonify, request
from model.venda import Venda
from model.query import Query
from pub import Pub
IP_HOST = "127.0.0.1"
PORTA = 8080
URL_API = f"http://{IP_HOST}:{PORTA}"
app = Flask(__name__)
query = Query()


@app.route("/cliente", methods=["GET", "POST"])
@app.route("/cliente/<int:id_cliente>", methods=["GET", "PUT", "DELETE"])
def cliente(id_cliente=None):
    if request.method == "GET":
        if id_cliente:
            try:
                cliente = query.clienteByID(id_cliente)
                return (jsonify(cliente.toJSON()), 200)
            except Exception as ex:
                return "", 404
        else:
            lista_clientes = []
            clientes = query.clienteAll()
            for cliente in clientes:
                lista_clientes.append(cliente.toJSON())
            return jsonify(lista_clientes), 200
    elif request.method == "POST":
        cliente = request.json
        query.clienteSave(cliente)
        return "", 201
    elif request.method == "PUT":
        cliente = request.json
        query.clienteUpdate(id_cliente, cliente)
        return "", 200
    elif request.method == "DELETE":
        query.clienteDelete(id_cliente)
        return "", 200


@app.route("/produto/<int:id_produto>", methods=["GET", "PUT", "DELETE", "POST"])
@app.route("/produto", methods=["GET", "POST"])
def produto(id_produto=None):
    if request.method == "GET":
        if id_produto:
            try:
                produto = query.produtoByID(id_produto)
                return (jsonify(produto.toJSON()), 200)
            except Exception as ex:
                return "", 404
        else:
            lista_produto = []
            produtos = query.produtoAll()
            for produto in produtos:
                lista_produto.append(produto.toJSON())
            return (jsonify(lista_produto), 200)
    elif request.method == "PUT":
        produto = request.json
        query.produtoUpdate(id_produto, produto)
        return ("", 200)
    elif request.method == "DELETE":
        query.produtoDelete(id_produto)
        return ("", 200)
    elif request.method == "POST":
        produto = request.json
        query.produtoSave(produto)
        return ("", 201)


@app.route("/venda", methods=["GET", "POST"])
def venda():
    if request.method == "GET":
        lista_vendas = []
        vendas = query.vendaAll()
        for venda in vendas:
            lista_vendas.append(venda.toJSON())
        return jsonify(lista_vendas), 200
    elif request.method == "POST":
        req = request.json
        try:
            tipo = req["tipo_pag"]
            # retorna o ultimo ID inserido
            id = query.vendaSave(req["cliente_id"], tipo, req["itens"])
            msg = {'ultimoID': id}
            # publica novo pagamento
            Pub(id, tipo).start()
            return msg, 201
        except Exception as ex:
            return "", 404


@app.route("/venda/<int:id_venda>", methods=["GET", "DELETE", "PUT"])
def venda_(id_venda):
    if request.method == "PUT":
        req = request.json
        print(req)
        query.vendaUpdateStatus(id_venda, req)
        return "", 200
    if request.method == "DELETE":
        query.vendaDelete(id_venda)
        return "", 200
    elif request.method == "GET":
        try:
            venda = query.vendaByID(id_venda)
            return (jsonify(venda.toJSON()), 200)
        except Exception as ex:
            return "", 404


@app.route("/status", methods=["GET"])
def venda__():
    if request.method == "GET":
        lista_vendas = []
        vendas = query.vendaAll()
        for venda in vendas:
            v: Venda = venda
            x = {
                'id': v.id,
                'tipo_pag': v.tipo_pag,
                "status": v.status
            }
            lista_vendas.append(x)
        return jsonify(lista_vendas), 200


app.run(host=IP_HOST, port=PORTA)
