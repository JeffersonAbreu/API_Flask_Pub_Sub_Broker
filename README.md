# API_Flask_Pub_Sub_Broker

<h1 align="center"> API - CRUD em Python</h1>
<h3 align="center">
    DB      = SQLite3<br>
    Flask   = ORM<br>
    API, Broker, Pub, Sub<br>
    <i>O exemplo simula um serviço de pagamento</i>
</h3>
<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge%22/%3E
</p>
<h4 align="center"> 
    🚧  Projeto foi desenvolvido na liguagem Python, com API com SQLite3 banco de dados  🚧
</h4>
# Resumo do projeto
CRUD    : Cliente, Produto e Venda.
ORM     : Acesso ao DB, querys...
Broker  : Simulando um serviço de pagamento onde ao finalizar a venda é disparado uma Pub ('publicação que há um nome pagamento').
Pub     : Está feita com Thread para melhor desempenho e desacoplamento. Responsável pela publicação dos TÓPICOS.
Sub     : Similar estrutura com threads e de responsabilidade de observar as publicação no broker.


## 🔨 Funcionalidades do projeto

- Requerimentos de execução do projeto: Se preferir apague o arquivo 'meubanco' dentro do diretório db. Vamos começar do zero!
- Execute no terminal: broker.py, api.py, pagamento.py (deixe visivel para observação dos logs)
- Execute no terminal: dentro do diretório 'model' o arquivo app_popular_db.py (esses requistes podem ser feitos por outro programas com Insomnia, Plugin VSCODE: Thunder Client, outro...)<br>
Obs.: <i>Abra o navegador e acesse o endereço: <sua_url>:8080/status</i> e acopanhe <F5> a andamento<br><br>O arquivo api.py tem todas as rotas, confira lá!

## ✔️ Técnicas e tecnologias utilizadas

- Python 3 (sqlalchemy, flask, requests, ...)
- SQLite3 (sqlite3)
- Visual Studio Code

## 📁 Acesso ao projeto
Você pode acessar os arquivos do projeto clicando [aqui](https://github.com/JeffersonAbreu/API_Flask_Pub_Sub_Broker/tree/main).