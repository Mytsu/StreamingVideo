from threading import Thread
import select

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

    def run(self):
        """

        :return:
        """
        self.lock.acquire()
        readable, writable, exceptional = select.select(self.listaPortos, [], [])
        self.lock.release()
        for udp in readable:
            udp.recvfrom(1024)

    def add_buffer(self, cliente):
        self.lock.acquire()
        self.listaClientes.update({cliente: ([], [])})
        self.lock.release()

    def add_pacote(self, cliente, pacote, valor=0):
        self.lock.acquire()
        self.listaClientes[cliente][self.PACOTE].append(pacote)
        self.listaClientes[cliente][self.ACK].append(valor)
        self.lock.release()

    def add_porto(self, porto):
        self.lock.acquire()
        self.listaPortos.append(porto)
        self.lock.release()
