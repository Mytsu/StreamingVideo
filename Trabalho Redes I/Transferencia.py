from threading import Thread
import socket
from ControleEnvio import ControleEnvio


class Transferencia(Thread):
    def __init__(self, unidadecontrole):
        Thread.__init__(self)
        self.dest = None
        self.arquivo = None
        self.unidadecontrole = unidadecontrole
        self.controle = ControleEnvio(self.unidadecontrole)
        
    def run(self):
        """

        :return:
        """
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(('', 0))
        print('0')
        self.unidadecontrole.add_porto(udp)
        print('1')
        conteudo = self.leitura_arquivo()
        while conteudo != b'':
            self.controle.sendmsg(conteudo, self.dest, udp, tipomsg=2, usounidadecontrole=True)
            conteudo = self.leitura_arquivo()
        self.fechar_arquivo() # termino de transferencia
        self.unidadecontrole.remover_porto(udp)
        udp.close()
        print('2')

    def leitura_arquivo(self):
        """

        :return:
        """
        return self.arquivo.read(self.controle.buffersize)

    def fechar_arquivo(self):
        """

        :return:
        """
        return self.arquivo.close()
