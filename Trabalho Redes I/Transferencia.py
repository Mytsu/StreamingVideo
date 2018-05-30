from threading import Thread
import socket
from ControleEnvio import ControleEnvio


class Transferencia(Thread):
    def __init__(self, unidadecontrole):
        Thread.__init__(self)
        self.dest = None
        self.arquivo = None
        self.controle = ControleEnvio()
        self.unidadecontrole = unidadecontrole

    def run(self):
        """

        :return:
        """
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(('', 0))
        self.unidadecontrole.add_porto(udp)
        conteudo = self.leitura_arquivo()
        while conteudo != b'':
            self.controle.sendmsg(conteudo, self.dest, udp)

    def leitura_arquivo(self):
        """

        :return:
        """
        return self.arquivo.read(self.controle.buffersize)