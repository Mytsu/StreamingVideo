from threading import Thread
import socket
from ControleEnvio import ControleEnvio
from time import sleep


class Transferencia(Thread):
    def __init__(self, unidadecontrole, lock, meuip):
        Thread.__init__(self)
        self.dest = None
        self.arquivo = None
        self.unidadecontrole = unidadecontrole
        self.controle = ControleEnvio(self.unidadecontrole)
        self.caixadeaviso = []
        self.lock = lock
        self.meuip = meuip

    def run(self):
        """

        :return:
        """
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind((self.meuip, 0))
        self.unidadecontrole.add_porto(udp)
        udp.settimeout(1)
        conteudo = self.leitura_arquivo()
        seq = 0
        while conteudo != b'':
            seq = self.controle.sendmsg(
                conteudo, self.dest, udp, tipomsg=2, usounidadecontrole=True, seq_inicial=seq
            )
            conteudo = self.leitura_arquivo()

        self.fechar_arquivo()
        while self.checkavisos() != 1:
            self.unidadecontrole.verifica_liberacao_thread(self.dest)
            sleep(1)
        self.unidadecontrole.remover_cliente(self.checkavisos(), udp)
         # termino de transferencia

        flag = 1
        while flag:
            self.controle.sendmsg(
                'encerramento_lista'.encode('utf-8'), self.dest, udp, tipomsg=3,
                seq_inicial=seq

            )
            try:
                udp.recv(1024) # resposta do ultimo ack
                flag = 0
            except:
                flag = 1
        print('encerrado')
        udp.close()

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

    def checkavisos(self):
        """
        checar as msg da unidade de controle
        :return:
        """
        self.lock.acquire()
        try:
            if not self.caixadeaviso:
                return 0
            else:
                return self.caixadeaviso.pop(0)
        finally:
            self.lock.release()
