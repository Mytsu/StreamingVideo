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
        self.data = ''

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
        mensagem = ''
        try:
            mensagem = self.udp.recv(1024)
        except: # time out except
            print('Timeout erro')
            self.requisita_servidor()
        print(mensagem)
        self.checkmsg(mensagem)

    def desmonta_pacote(self, msg):
        """

        :param msg:
        :return:
        """
        return msg[:8], msg[8:]

    def checkmsg(self, msg):
        """

        :param msg:
        :return:
        """
        head, data = self.desmonta_pacote(msg)
        tipo = int().from_bytes(head[7:8], 'big')
        numero_seq = int().from_bytes(head[:4], 'big')
        windowsize = int().from_bytes(head[4:7], 'big')
        # check header
        self.tratamento(data, tipo)

        return data

    def tratamento(self, data, tipo):
        """

        :param data:
        :param tipo:
        :return:
        """
        if tipo == 0:
            data = data.decode('utf-8')
            if 'encerramento_lista' not in data:
                self.data = self.data + data
                self.recebermsg()
            else:
                arquivos = self.data.split('#')
                for arquivo in arquivos:
                    print(arquivo)


if __name__ == '__main__':
    cliente = Cliente()
    cliente.requisita_servidor()