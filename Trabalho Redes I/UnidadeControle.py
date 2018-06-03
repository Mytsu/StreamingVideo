from threading import Thread
import select
from time import sleep
import socket
from Pacote import Pacote


class UnidadeControle(Thread):
    (
        PACOTE,
        ACK,
        TIME
    ) = range(3)

    def __init__(self, lock):
        Thread.__init__(self)
        self.listaClientes = {}
        self.threadsusadas = {}
        self.lock = lock
        self.listaPortos = []
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.settimeout(1)
        self.timeoutpacote = 3

    def run(self):
        """

        :return:
        """

        while True:
            if self.listaPortos: # lista dos portos para se analisar os acks
                print('olhando leitura')
                self.lock.acquire()
                readable, writable, exceptional = select.select(self.listaPortos, [], [], self.udp.gettimeout())
                self.lock.release()
                for udp in readable:
                    msg, cliente = udp.recvfrom(1024) # recebimento do ack
                    print(msg)
                    self.tratamsg(msg, cliente)


                # verifica se algum pacote deu o timeout e libera o pacote do buffer
                self.verifica_timeout_pacote()
                # verifica se posso liberar alguma thread
                self.verifica_liberacao_thread()
            else:
                sleep(3)

    def add_buffer(self, cliente, threferente):
        """
        Buffer do controle de envio
        :param cliente: cliente a receber o envio
        :param threferente: thread a tratar do envio
        :return:
        """
        self.lock.acquire()
        self.listaClientes.update({cliente: []})
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
        self.listaClientes[cliente].append(Pacote(pacote, valor, self.timeoutpacote))
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
        print('AVISO PARA THREAD')
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

        self.lock.acquire()

        numero_seq = int(data.decode('utf-8'))
        print(numero_seq)
        for pacote in self.listaClientes[cliente]:
            if int().from_bytes(pacote.dados[:4], 'big') == numero_seq:
                pacote.ack = 1
                print('liberei alguem')
                self.listaClientes[cliente].remove(pacote)

        self.lock.release()

    def desmonta_pacote(self, msg):
        """

        :param msg:
        :return:
        """
        return msg[:8], msg[8:]

    def verifica_timeout_pacote(self):
        """

        :return:
        """
        self.lock.acquire()
        for cliente in self.listaClientes.keys():
            for pacote in self.listaClientes[cliente]:
                if pacote.ack == 1:
                    continue
                pacote.time -= 1
                if pacote.time <= 0:
                    pacote.time = 10
                    self.udp.sendto(pacote.dados, cliente)
        self.lock.release()

    def verifica_liberacao_thread(self):
        marcado = []
        self.lock.acquire()
        for cliente in self.listaClientes.keys():
            if not self.listaClientes[cliente]:
                self.avisar_thread(self.threadsusadas[cliente], 1)
                self.threadsusadas.pop(cliente)
                marcado.append(cliente)
        for m in marcado:
            self.listaClientes.pop(m)
        self.lock.release()