import socket
from ControleEnvio import ControleEnvio


class Cliente(object):
    def __init__(self, ipservidor=socket.gethostbyname(socket.gethostname())):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.meuip = socket.gethostbyname(socket.gethostname())
        orig = (self.meuip, 0)
        self.udp.bind(orig)
        self.meuporto = self.udp.getsockname()
        self.servidor = (ipservidor, 50000)
        self.controle = ControleEnvio()
        self.udp.settimeout(1)

    def requisita_servidor(self):
        """

        :return:
        """
        mensagem = input('> ')
        self.controle.sendmsg(mensagem, self.servidor, self.udp)
        self.recebermsg()

    def recebermsg(self):
        """

        :return:
        """
        mensagem = ''
        try:
            mensagem = self.udp.recv(1024)
        except TimeoutError:
            print('Timeout erro')
            self.requisita_servidor()

        self.checkmsg(mensagem)

    def desmonta_pacote(self, msg):
        """

        :param msg:
        :return:
        """
        ba = bytearray(msg)
        print(msg)
        return ba[:8], ba[8:]

    def checkmsg(self, msg):
        """

        :param msg:
        :return:
        """
        head, data = self.desmonta_pacote(msg)
        # check header
        print(data.decode('utf-8'))


if __name__ == '__main__':
    cliente = Cliente()
    cliente.requisita_servidor()