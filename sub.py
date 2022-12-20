import zmq
import requests

from threading import Thread

class Sub(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.IP_ADDRESS = "127.0.0.1"
        self.TOPIC = f"TOPIC_{id}"
        self.ctx = zmq.Context()
        self.sock : zmq.Socket = self.ctx.socket(zmq.SUB)
        self.repetir = True
        self.statusOld = ''
        self.id = id

    def run(self):
        self.sock.connect(f"tcp://{self.IP_ADDRESS}:5501")
        print(f"TOPICO:  {self.TOPIC} no guardando!")
        self.sock.subscribe(self.TOPIC)
        while self.repetir:
            msg_string = self.sock.recv_string()
            msg_json = self.sock.recv_json()
            status = msg_json['status']
            print(f"{msg_json['tipo']} do topico {msg_string}.")
            if(status == 'OK'):
                self.repetir = False
            else:
                if(status != self.statusOld):
                    url = "http://127.0.0.1:8080"
                    requests.put(f"{url}/venda/{self.id}", json={"status": status})
                self.statusOld = status

        self.sock.close()
        self.ctx.term()
        print('======================= TERMINOU =========================')

if __name__ == "__main__":
    Sub(1).start()