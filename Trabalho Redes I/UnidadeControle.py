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
        self.threadsusadas = {}
        self.lock = lock
        self.listaPortos = []
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.settimeout(1)

    def run(self):
        """

        :return:
        """

        while True:
            if self.listaPortos: # lista dos portos para se analisar os acks
                self.lock.acquire()
                readable, writable, exceptional = select.select(self.listaPortos, [], [], self.udp.gettimeout())
                self.lock.release()

                for udp in readable:
                    msg, cliente = udp.recvfrom(1024) # recebimento do ack
                    self.tratamsg(msg, cliente)
                sleep(5)
            else:
                sleep(5)

    def add_buffer(self, cliente, threferente):
        """
        Buffer do controle de envio
        :param cliente: cliente a receber o envio
        :param threferente: thread a tratar do envio
        :return:
        """
        self.lock.acquire()
        self.listaClientes.update({cliente: ([], [])})
        self.threadsusadas.update({cliente: threferente})
        self.lock.release()

    def add_pacote(self, cliente, pacote, valor=0):
        """
        Adiciona um pacote ao buffer de envio
        :param cliente: cliente que foi enciado o pacote
        :param pacote: pacote enviado
        :param valor: 0 quando ainda nao recebeu o pacote e ack quando receber
        :return:
        """
        self.lock.acquire()
        self.listaClientes[cliente][self.PACOTE].append(pacote)
        self.listaClientes[cliente][self.ACK].append(valor)
        self.lock.release()

    def add_porto(self, udp):
        """
        add porto onde sera recebido os acks da transferencia
        :param udp: porto onde esta amarrado a conn
        :return:
        """
        self.lock.acquire()
        self.listaPortos.append(udp)
        self.lock.release()

    def remover_porto(self, udp):
        self.lock.acquire()
        self.listaPortos.remove(udp)
        self.lock.release()

    def avisar_thread(self, th, aviso):
        """
        Avisar a thread: se ela pode terminar se ela deve reenviar algum arquivo ou se pode continuar enviando
        :param th: thread a ser avisada
        :param aviso: menssagem para a thread
        :return:
        """
        print(aviso)
        th.lock.acquire()
        th.caixadeaviso.append(aviso)
        th.lock.release()

    def tratamsg(self, msg, cliente):
        """
        verifica o ack recebido
        :param msg: mensagem inteira com o numero de sequencia confirmado pelo ack
        :return:
        """
        head, data = self.desmonta_pacote(msg)
        tipo = int().from_bytes(head[7:8], 'big')

        if tipo != 4:
            return 0

        numero_seq = int(data.encode('utf-8'))
        self.lock.acquire()
        self.listaClientes[cliente][self.ACK][numero_seq] = 1
        self.lock.release()

    def desmonta_pacote(self, msg):
        """

        :param msg:
        :return:
        """
        return msg[:8], msg[8:]
