import socket
from ControleEnvio import ControleEnvio


class Cliente(object):
    def __init__(self, ipservidor=socket.gethostbyname(socket.gethostname())):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.meuip = socket.gethostbyname(socket.gethostname())
        orig = (self.meuip, 0)
        self.udp.bind(orig)
        self.meuporto = self.udp.getsockname()
        self.servidor = ('127.0.1.1', 50000)
        self.controle = ControleEnvio()
        self.udp.settimeout(1)
        self.buffer = None
        self.arquivo = None

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

        self.checkmsg(mensagem, srvenvio)
        self.requisita_servidor()

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
            data = data.decode('utf-8')

            self.buffer = self.buffer + data
            self.recebermsg()

        if tipo == 1: # inicio transferencia de arquivo
            # inserindo primeiro pacote na lista
            self.buffer += data
            mensagem = str(numero_seq)
            self.controle.sendmsg(mensagem, srvenvio, self.udp, tipomsg=4)
        if tipo == 2:
            self.buffer += data
            mensagem = str(numero_seq)
            self.controle.sendmsg(mensagem, srvenvio, self.udp, tipomsg=4)
        if tipo == 3:
            arquivos = self.buffer.split('#')
            for arquivo in arquivos:
                print(arquivo)


if __name__ == '__main__':
    cliente = Cliente()
    cliente.requisita_servidor()