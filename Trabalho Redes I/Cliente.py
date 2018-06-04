import socket
from ControleEnvio import ControleEnvio
import sys
import random


class Cliente(object):
    def __init__(self, meuip= socket.gethostbyname(socket.gethostname()), ipservidor=socket.gethostbyname(socket.gethostname())):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.meuip = meuip
        orig = (self.meuip, 0)
        self.udp.bind(orig)
        self.meuporto = self.udp.getsockname()
        self.servidor = (ipservidor, 50000)
        self.controle = ControleEnvio()
        self.udp.settimeout(1)
        self.buffer = b''
        self.arquivo = None
        self.pacotes_recebidos = []

    def requisita_servidor(self):
        """

        :return:
        """
        mensagem = input('> ')
        self.controle.sendmsg(mensagem, self.servidor, self.udp, tipomsg=2)
        self.recebermsg()

    def recebermsg(self):
        """

        :return:
        """
        srvenvio = ''
        mensagem = ''
        try:
            mensagem, srvenvio = self.udp.recvfrom(1024)
        except: # time out except
            print('Timeout erro')
            self.requisita_servidor()

        print(srvenvio)
        self.checkmsg(mensagem, srvenvio)

    def desmonta_pacote(self, msg):
        """

        :param msg:
        :return:
        """
        return msg[:8], msg[8:]

    def checkmsg(self, msg, srvenvio):
        """

        :param msg:
        :return:
        """
        head, data = self.desmonta_pacote(msg)
        tipo = int().from_bytes(head[7:8], 'big')
        numero_seq = int().from_bytes(head[:4], 'big')
        windowsize = int().from_bytes(head[4:7], 'big')
        # check header
        self.tratamento(data, tipo, numero_seq, windowsize, srvenvio)

    def tratamento(self, data, tipo, numero_seq, windowsize,  srvenvio):
        """

        :param data:
        :param tipo:
        :return:
        """
        if tipo == 0:
            self.buffer = self.buffer + data
            self.recebermsg()

        if tipo == 1: # inicio transferencia de arquivo
            # inserindo primeiro pacote na lista
            print(windowsize)
            self.pacotes_recebidos = bytearray(windowsize+1)
            print(self.pacotes_recebidos)
            self.buffer += data
            self.pacotes_recebidos[numero_seq] = 1
            mensagem = str(numero_seq)
            print(numero_seq)
            self.controle.sendmsg(mensagem, srvenvio, self.udp, tipomsg=4)
            self.recebermsg()
        if tipo == 2:
            self.buffer += data
            mensagem = str(numero_seq)
            print(numero_seq)
            self.pacotes_recebidos[numero_seq] = 1
            self.controle.sendmsg(mensagem, srvenvio, self.udp, tipomsg=4)
            self.recebermsg()
        if tipo == 3:
            print(numero_seq)
            mensagem = str(numero_seq)
            self.pacotes_recebidos[numero_seq] = 1
            self.controle.sendmsg(mensagem, srvenvio, self.udp, tipomsg=4)

        print(self.pacotes_recebidos)
        if not all(self.pacotes_recebidos):
            self.recebermsg()
        else:
            self.requisita_servidor()


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        cliente = Cliente(sys.argv[1], sys.argv[2])
    else:
        cliente = Cliente()

    cliente.requisita_servidor()