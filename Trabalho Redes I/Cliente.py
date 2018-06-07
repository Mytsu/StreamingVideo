import socket
from ControleEnvio import ControleEnvio
import sys
import random
import os
import threading
from Pacote import Pacote
from Video import Video

class Cliente(object):
    def __init__(self, meuip= socket.gethostbyname(socket.gethostname()), ipservidor=socket.gethostbyname(socket.gethostname())):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.meuip = meuip
        orig = (self.meuip, 0)
        self.udp.bind(orig)
        self.meuporto = self.udp.getsockname()
        self.servidor = (ipservidor, 50000)
        self.controle = ControleEnvio()
        self.udp.settimeout(10)
        self.buffer = []
        self.arquivo = None
        self.pacotes_recebidos = []
        self.num_pacotes = 0
        self.video = Video()

    def requisita_servidor(self):
        """

        :return:
        """

        mensagem = input('> ')
        self.video.start()
        self.controle.sendmsg(mensagem, self.servidor, self.udp, tipomsg=2)
        self.num_pacotes = 0

        msg, srv = self.recebermsg()
        while msg is not None:
            self.tratamento(msg, srv)
            msg, srv = self.recebermsg()

    def recebermsg(self):
        """

        :return:
        """
        srvenvio = ''
        mensagem = ''
        try:
            mensagem, srvenvio = self.udp.recvfrom(1024)
        except: # time out except
            print('time error')
            return None, None



        return mensagem, srvenvio
        #self.checkmsg(mensagem, srvenvio)

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
        return data, tipo, numero_seq, windowsize
        #self.tratamento(data, tipo, numero_seq, windowsize, srvenvio)

    def tratamento(self, msg, srv):
        """

        :param data:
        :param tipo:
        :return:
        """
        numero_grande = (2 ** 32) - 1
        data, tipo, numero_seq, windowsize = self.checkmsg(msg, srv)

        if tipo == 0:
            arquivos = (data.decode('utf-8')).split('#')
            i = 0
            for arquivo in arquivos:
                print(str(i) + ': ' + arquivo)
                i += 1

            return 1

        if tipo == 1: # inicio transferencia de arquivo
            # inserindo primeiro pacote na lista

            #self.pacotes_recebidos = bytearray(self.controle.buffersize + 1) # verificar se recebi todos os pacotes
            self.num_pacotes += 1               # auxiliar na verificacao da ordenacao
            self.arquivo = open('video', 'wb')  # cria o arquivo mp4, que ira conter o video
            self.arquivo.write(data)
           # self.pacotes_recebidos[numero_seq] = 1
            mensagem = str(numero_seq)
            self.controle.sendmsg(mensagem, srv, self.udp, tipomsg=4)
            #video = threading.Thread(target=worker())
           # video.start()

            return 1
        if tipo == 2:
            # se for igual entao esta na ordem
            print("%d %d" %(numero_seq, self.num_pacotes))
            if numero_seq % numero_grande == self.num_pacotes:
                self.num_pacotes += 1
                self.arquivo.write(data)
                self.buffer.sort(key=lambda x: x.numseq)
                #self.arquivo.writelines([i.dados for i in self.buffer])
                self.num_pacotes += len(self.buffer)
                self.buffer = []
            elif (numero_seq % numero_grande) > self.num_pacotes: # esta fora de ordem
                self.arquivo.write(data)
                self.buffer.append(Pacote(data, 0, numero_seq))

                # executar thread que ira rodar o video

            mensagem = str(numero_seq)

            #self.pacotes_recebidos[numero_seq] = 1

            self.controle.sendmsg(mensagem, srv, self.udp, tipomsg=4)

            return 1
        if tipo == 3:
            print("%d %d" % (numero_seq, self.num_pacotes))
            mensagem = str(numero_seq)
            #self.pacotes_recebidos[numero_seq] = 1
            self.controle.sendmsg(mensagem, srv, self.udp, tipomsg=4)

        self.buffer.sort(key=lambda x: x.numseq)
        #self.arquivo.writelines([i.dados for i in self.buffer])
        self.num_pacotes += len(self.buffer)
        self.buffer = []

        if not all(self.pacotes_recebidos):
            return 1
        else:
            self.arquivo.close()
            return 1


def worker():
    os.system('mpv video')


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        cliente = Cliente(sys.argv[1], sys.argv[2])
    else:
        cliente = Cliente()

    cliente.requisita_servidor()