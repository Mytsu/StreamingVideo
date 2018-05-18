from threading import Thread
import socket
import os

class Transferencia(Thread):
    def __init__(self, num):
        Thread.__init__(self)
        self.num = num
        self.nome = None
        self.dest = None
        self.buffleitura = 2048

    @property
    def arquivo(self):
        """
        procura o nome do arquivo
        :return: nome do arquivo ou 0 caso nao encontrado
        """
        self.nome = self.nome.decode()
        comandos = self.nome.split(" ")
        print(comandos)
        diretorio = (os.path.dirname(os.path.realpath(__file__))) + "/streamer/" + comandos[1]
        print(diretorio)
        try:
            self.arq = open(diretorio, "rb")
        except FileNotFoundError:
            print("nao deu")
            return None

        return self.nome                       # se ok return nome do arquivo

    def run(self):
        """
        Transferencia do arquivo
        :return:
        """
        if not self.arquivo:
            return -1                         # enviar menssagem de erro ao cliente

        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = 'passar'.encode("utf-8")
        contamsg = 0
        while msg != b'':
            contamsg += 1
            msg = contamsg.encode()
            msg = msg + self.arq.read(self.buffleitura)  # leitura de n bits do arquivo
            udp.sendto(msg, self.dest)

        udp.close()


