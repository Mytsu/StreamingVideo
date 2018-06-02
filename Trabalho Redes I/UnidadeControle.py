from threading import Thread
import select
from time import sleep
import socket


class UnidadeControle(Thread):
    (
        PACOTE,
        ACK
    ) = range(2)

    def __init__(self, lock):
        Thread.__init__(self)
        self.listaClientes = {}
        self.lock = lock
        self.listaPortos = []
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.settimeout(1)

    def run(self):
        """

        :return:
        """

        while True:
            if not self.listaPortos:
                self.lock.acquire()
                readable, writable, exceptional = select.select(self.listaPortos, [], [], self.udp.gettimeout())
                self.lock.release()

                for udp in readable:
                    msg, cliente = udp.recvfrom(1024)
                    print(msg)
                sleep(5)
            else:
                sleep(5)

    def add_buffer(self, cliente):
        self.lock.acquire()
        self.listaClientes.update({cliente: ([], [])})
        self.lock.release()

    def add_pacote(self, cliente, pacote, valor=0):
        self.lock.acquire()
        self.listaClientes[cliente][self.PACOTE].append(pacote)
        self.listaClientes[cliente][self.ACK].append(valor)
        self.lock.release()

    def add_porto(self, udp):
        self.lock.acquire()
        self.listaPortos.append(udp)
        self.lock.release()

    def remover_porto(self, udp):
        self.lock.acquire()
        self.listaPortos.remove(udp)
        self.lock.release()
