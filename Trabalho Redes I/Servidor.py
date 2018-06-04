import socket
import os
from ControleEnvio import ControleEnvio
from UnidadeControle import UnidadeControle
from threading import Thread, Lock
from Transferencia import Transferencia
import sys


class Servidor(object):
    def __init__(self, meuip=socket.gethostbyname(socket.gethostname()), diretorio='/streamer', arquivolog= 'meulog.log'):
        self.diretorio = (os.path.dirname(os.path.realpath(__file__))) + "/streamer/"
        self.poolThreads = []
        # criar conexao udp
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        HOST = meuip
        PORT = 50000
        # define arquivo de log
        try:
            self.arquivolog = open(arquivolog, "r")
            self.conteudo = self.arquivolog.readlines()
        except FileNotFoundError:
            self.arquivolog = open(arquivolog, "w")
            self.conteudo = []

        # tentativas de se amarrar porto, para uso exclusivo do servidor
        orig = (HOST, PORT)
        self.udp.bind(orig)
        print('Endereco servidor :' + str(orig))
        # diretorio onde estara os videos no servidor
        self.diretorio_arquivos = (os.path.dirname(os.path.realpath(__file__))) + diretorio
        self.build_thread_control()
        self.controle = ControleEnvio(self.unidadeControle)
        self.build_threads()

    def build_thread_control(self):
        self.lock = Lock()
        self.unidadeControle = UnidadeControle(self.lock)
        self.unidadeControle.start()

    def build_threads(self):
        """
        Criando a pool de threads do servidor
        :return:
        """
        self.poolThreads = [Transferencia(self.unidadeControle, Lock()) for i in range(10)]

    def wait(self):
        """
        A espera de uma requisicao do cliente
        :return:
        """
        print('Servidor a espera de requisicao')
        while True:
            # menssagem do cliente e seu especifico (ip, porto) para transferencia de dados
            msg, cliente = self.udp.recvfrom(1024)
            print('Login: ' + str(cliente))
            self.conteudo.append('Login: ' + str(cliente))
            self.accept(msg, cliente)

    def accept(self, msg, cliente):
        """
        Requisicao aceita:
            verificacao de threads em espera na pool e passagem do cliente para a thread
        :return:
        """
        data = self.checkmsg(msg)
        arquivos = [os.path.join(nome) for nome in os.listdir(self.diretorio_arquivos)]
        # informando os videos presentes para transferencia
        if 'arquivos lista' in data:
            self.controle.sendmsg('#'.join(arquivos), cliente, self.udp, tipomsg=0)

        elif 'get' in data:
            prm = data.split(" ")
            try:
                arquivo = open(self.diretorio + arquivos[int(prm[1])], 'rb')
                for th in self.poolThreads:
                    if not th.isAlive():
                        self.unidadeControle.add_buffer(cliente, th)
                        th.dest = cliente
                        th.arquivo = arquivo
                        th.start()
                        self.poolThreads.remove(th)
                        self.poolThreads.append(Transferencia(self.unidadeControle, Lock()))
                        break

            except ValueError:
                self.controle.sendmsg('erro index invalido', cliente, self.udp, tipomsg=0)
            except IndexError:
                self.controle.sendmsg('erro index invalido', cliente, self.udp, tipomsg=0)
            except FileNotFoundError:
                self.controle.sendmsg('erro arquivo nao encontrado', cliente, self.udp, tipomsg=0)

        self.wait()

    def checkmsg(self, msg):
        """

        :param msg: msg em formato utf-8
        :return: cabecario, dados
        """
        ba = bytearray(msg)
        head = ba[:8]
        # retorno somente da msg

        return msg[8:].decode('utf-8')


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        servidor = Servidor(sys.argv[1])
    else:
        servidor = Servidor()
    servidor.wait()
