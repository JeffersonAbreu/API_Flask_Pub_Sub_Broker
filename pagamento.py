import concurrent.futures
import logging
import threading
import time
import zmq
from sub import Sub
PAGAMENTOS: list = list()

def getPrimeiroPagamentoFila():
    pagamento = PAGAMENTOS.pop(0)
    logging.debug(f"> Pegando o primeiro pagamento da fila. ({pagamento['tipo']})")
    return pagamento


def setPagamentoFinalDaFila(pagamento):
    name = f"{pagamento['tipo']} : {pagamento['id']}"
    logging.debug(f"{name}: Adicionando pagamento ao final da fila.")
    PAGAMENTOS.append(pagamento)


def existe():
    return size() > 0


def size() -> int:
    return len(PAGAMENTOS)


def atualizadorStatusPagamento():
    IP_ADDRESS = "127.0.0.1"
    _TOPIC = ""
    ctx = zmq.Context()
    sock: zmq.Socket = ctx.socket(zmq.PUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5500")
    try:
        while True:
            #  espera para simular o tempo para validação da venda
            time.sleep(2)
            if (existe()):
                print('\n')
                logging.info(f"   >>>  fila de pagamento: {size()} pagamentos")
                # primeiro da fila de processos
                pgto = getPrimeiroPagamentoFila()
                id = pgto['id']
                loop = pgto['loop']
                if (loop == 4):
                    pgto['status'] = "VALIDANDO PAGAMENTO"
                elif (loop == 2):
                    pgto['status'] = "PROCESSANDO"
                elif (loop == 0):
                    pgto['status'] = "APROVADO"
                elif (loop < 0):
                    pgto['status'] = "OK"
                _TOPIC = f"TOPIC_{id}"
                sock.send_string(f"{_TOPIC}", flags=zmq.SNDMORE)
                sock.send_json(pgto)
                logging.info(f"      {_TOPIC} => {pgto['status']} ( loop restantes {pgto['loop']})")
                loop -= 1

                 # se status OK, não coloca na fila de pagamentos a ser processada
                if (loop >= 0):
                    pgto['loop'] = loop
                    setPagamentoFinalDaFila(pgto)

    except Exception as e:
        print("=============================   ERRO   ===============================")
        print(e)
    finally:
        sock.close()
        ctx.term()


def observandoNewPagamento():
    IP_ADDRESS = "127.0.0.1"
    TOPIC = "pagamento"
    ctx = zmq.Context()
    sock: zmq.Socket = ctx.socket(zmq.SUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5501")
    sock.subscribe(f"{TOPIC}")
    logging.info(f"Iniciando serviço de {TOPIC}!")
    try:
        while True:
            msg = sock.recv_string()
            dados = sock.recv_json()
            if (len(dados) != 0):
                print('')
                logging.debug(f"Nova requisição de {msg} recebida:   {dados}")
                print('')
                threading.Thread(target=start(dados=dados), daemon=True).start()
    except Exception as e:
        print(f"=========================================    ERRO    =========================================")
        print(e)
    finally:
        sock.close()
        ctx.term()

def start(dados):
    id = dados['id']
    status = 'AGUARDANDO PAGAMENTO'
    loop = 0
    tipo = dados['tipo']
    if (tipo == 'pix'):
        loop = 5
    elif (tipo == 'boleto'):
        loop = 15
    elif (tipo == 'cartao'):
        loop = 10
    newPagamento = {
        'id'    : id,
        'status': status,
        'tipo'  : tipo,
        'loop'  : loop
    }
    logging.info(newPagamento)
    # cria novo pagamento
    setPagamentoFinalDaFila(newPagamento)
    # new_thread Sub
    Sub(id).start()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    # descomente a linha abaixo pra ver os logs
    # logging.getLogger().setLevel(logging.DEBUG)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(atualizadorStatusPagamento)
        executor.submit(observandoNewPagamento)