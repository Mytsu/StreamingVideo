import math
from time import sleep


class ControleEnvio(object):
    def __init__(self, unidadecontrole = None):
        self.buffersize = 100000 # 8 mb
        self.windowsize = 100000
        self.unidadecontrole = unidadecontrole

    def sendmsg(self, msg, cliente, udp, tipomsg, usounidadecontrole=False, seq_inicial = 0):
        """
        formata a msg para envio
        :param msg: msg a ser enviada
        :return:
        """
        if type(msg) == str:
            msg = msg.encode('utf-8')

        lista_msg = self.fragmenta(msg)
        self.windowsize = len(lista_msg)
        pacote = ''
        cont = seq_inicial
        numero_grande = (2 ** 32) - 1
        for mensagem in lista_msg:
            sleep(0.002)
            if (cont+1)%500 == 0:
                sleep(1)
            if (cont == 0) and (tipomsg != 0) and (tipomsg != 4):
                pacote = self.adiciona_cabecalho(mensagem, cont % numero_grande, tipomsg=1)
            else:
                pacote = self.adiciona_cabecalho(mensagem, cont % numero_grande, tipomsg)

            if usounidadecontrole:
                self.unidadecontrole.add_pacote(cliente, pacote, cont)

            udp.sendto(pacote, cliente)
            cont += 1

        return cont

    def fragmenta(self, msg):
        # em bytes
        tamanho = len(msg)

        # 1024 tamanho do pacote
        numero_pacotes = math.ceil(tamanho / 1016)

        lista_envio = []
        for i in range(int(numero_pacotes)):
            if 1016*i+1016 <= len(msg):
                lista_envio.append(msg[1016*i:1016*i+1016])
            else:
                lista_envio.append(msg[1016 * i:len(msg)])

        return lista_envio

    def adiciona_cabecalho(self, msg, numero_sequencia, tipomsg):
        """

        :param numero_sequencia:
        :return:
        """
        head = numero_sequencia.to_bytes(4, 'big')
        cabecalho = head+self.windowsize.to_bytes(3, 'big') + tipomsg.to_bytes(1, 'big')
        return cabecalho + msg