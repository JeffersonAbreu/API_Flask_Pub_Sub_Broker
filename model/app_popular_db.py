#!/usr/bin/env python3
import requests
from pprint import pprint

url = "http://127.0.0.1:8080"

produtos = [
    {"nome": "Honda Fan 160", "preco": 16000.00},
    {"nome": "Yamaha FZ15", "preco": 18000.00},
    {"nome": "Kawazaki Ninja 300", "preco": 22000.00},
    {"nome": "Gol G6 1.4", "preco": 1000.00},
    {"nome": "Peugeout 206 1.6", "preco": 12000.00},
    {"nome": "Hyundai HB20 1.6 Aut", "preco": 15999.00},
    {"nome": "Honda Fit 1.5 VTEC", "preco": 13009.99}
]

clientes = [
    {"nome": "Amanda", "endereco": "Rua 456"},
    {"nome": "Carolina", "endereco": "Rua asd"},
    {"nome": "Daniel", "endereco": "Rua dfg"},
    {"nome": "Viviane", "endereco": "Rua 4d"},
    {"nome": "Theo", "endereco": "Rua dfgg6"},
    {"nome": "Ricardo", "endereco": "Rua dfgg"},
    {"nome": "Antonio", "endereco": "Rua dfggd"}
]

vendas = [
    {
        "cliente_id": 1,
        "tipo_pag": 'boleto',
        "itens":
        [
            {
                "produto_id": 1,
                "qtd": 2,
                "preco": 10.00
            }, {
                "produto_id": 2,
                "qtd": 1,
                "preco": 9.99
            }
        ]
    },
    {
        "cliente_id": 2,
        "tipo_pag": 'pix',
        "itens":
        [
            {
                "produto_id": 1,
                "qtd": 2,
                "preco": 10.00
            }, {
                "produto_id": 2,
                "qtd": 1,
                "preco": 9.99
            }
        ]
    },
    {
        "cliente_id": 4,
        "tipo_pag": 'cartao',
        "itens":
        [
            {
                "produto_id": 1,
                "qtd": 2,
                "preco": 10.00
            }, {
                "produto_id": 2,
                "qtd": 1,
                "preco": 9.99
            }
        ]
    }
]

for cliente in clientes:
    requests.post(f"{url}/cliente", json=cliente)

r = requests.get(f"{url}/cliente")
pprint(r.json())

for produto in produtos:
    requests.post(f"{url}/produto", json=produto)

r = requests.get(f"{url}/produto")
pprint(r.json())

for venda in vendas:
    requests.post(f"{url}/venda", json=venda)

r = requests.get(f"{url}/venda")
pprint(r.json())