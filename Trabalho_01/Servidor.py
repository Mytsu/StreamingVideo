from Transferencia import Transferencia
import socket
import os


class Servidor(object):

    def __init__(self):
        self.poolThreads = []
        for i in range(10):
            self.poolThreads.append(Transferencia(i))
        HOST = '10.120.7.45'  # Endereco IP do Servidor
        PORT = 5000  # Porta que o Servidor esta
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        orig = (HOST, PORT)
        self.udp.bind(orig)
        self.diretorio_arquivos = (os.path.dirname(os.path.realpath(__file__))) + "/streamer"

    def esperaRequisicao(self):
        """
        espera requisicao do cliente e manda para uma das threads
        :return:
        """
        while True:
            msg, cliente = self.udp.recvfrom(1024)
            print(cliente)
            if 'arquivos lista'.encode('utf-8') in msg:
                arquivos = [os.path.join(nome.encode('utf-8')) for nome in os.listdir(self.diretorio_arquivos)]
                for arquivo in arquivos:
                    self.udp.sendto(arquivo, cliente)
                self.udp.sendto('encerramento_lista'.encode('utf-8'), cliente)
            elif 'get'.encode('utf-8') in msg:
                for th in self.poolThreads:
                    if not th.isAlive():
                        th.dest = cliente
                        th.nome = msg
                        th.run()
                        break



if __name__ == '__main__':
    s = Servidor()
    s.esperaRequisicao()