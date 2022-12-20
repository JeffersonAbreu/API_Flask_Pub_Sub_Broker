import zmq
import time
from threading import Thread
import logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


class Pub(Thread):
    def __init__(self, id, tipo):
        Thread.__init__(self)
        self.id = id
        self.tipo = tipo
        self.IP_ADDRESS = "127.0.0.1"
        self.TOPIC = 'pagamento'
        self.ctx = zmq.Context()
        self.sock: zmq.Socket = self.ctx.socket(zmq.PUB)

    def run(self):
        try:
            self.sock.connect(f"tcp://{self.IP_ADDRESS}:5500")
            # não remover
            time.sleep(1)
            logging.debug(f"\nTOPIC: {self.TOPIC}\n   ID: {self.id}\n TIPO: {self.tipo}")
            self.sock.send_string(f"{self.TOPIC}", flags=zmq.SNDMORE)
            self.sock.send_json({"id": self.id, "tipo": self.tipo})
        except Exception as e:
            logging.warning(f"bringing down zmq device: error -> {e}")
        finally:
            self.sock.close()
            self.ctx.term()


if __name__ == "__main__":
    Pub(1, 'boleto').start()
    time.sleep(1)
    Pub(2, 'pix').start()
    time.sleep(1)
    Pub(3, 'cartao').start()
    time.sleep(1)
    Pub(4, 'boleto').start()
    time.sleep(1)
