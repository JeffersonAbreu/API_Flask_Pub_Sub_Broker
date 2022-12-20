import zmq
import requests
IP_HOST = "127.0.0.1"
URL_API = f"http://{IP_HOST}:8080"

from threading import Thread

class Sub(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.URL = f"tcp://{IP_HOST}:5501"
        self.TOPIC = f"TOPIC_{id}"
        self.ctx = zmq.Context()
        self.sock : zmq.Socket = self.ctx.socket(zmq.SUB)
        self.repetir = True
        self.statusOld = ''
        self.id = id

    def run(self):
        self.sock.connect(self.URL)
        print(f"TOPICO:  {self.TOPIC} no guardando!")
        self.sock.subscribe(self.TOPIC)
        while self.repetir:
            msg_string  = self.sock.recv_string()
            msg_json    = self.sock.recv_json()
            status = msg_json['status']
            if(status == 'OK'):
                self.repetir = False
            else:
                if(status != self.statusOld):
                    requests.put(f"{URL_API}/venda/{self.id}", json={"status": status})
                self.statusOld = status

        self.sock.close()
        self.ctx.term()
        print('======================= TERMINOU =========================')

if __name__ == "__main__":
    Sub(1).start()