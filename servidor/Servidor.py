import socket
import argparse
from Pacote import Controle
from Arquivo import Arquivo
from ast import literal_eval
from time import sleep


class Servidor(object):
    """
        Servidor para transferencia de video
    """
    (
        GET,
        PAUSE,
        SEEK,
        BACK,
        TRANS,
        ACK,
        PLAY
    ) = range(7)

    def __init__(self, ip_porto):
        """

        :param ip_porto: tupla contento ip e porto da conexao tcp
        """

        # instanciando as variaveis da conexao TCP e UDP
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # salvando o ip do servidor
        self.meuip = ip_porto[0]

        # Amarrando a porta do TCP e criando uma lista de dependencias de tamanho 1
        self.tcp.bind(ip_porto)
        self.tcp.listen(1)

        # variaveis de controle
        self.tamdados = 1020    # bytes de dados dentro do pacote
        self.bufferread = self.tamdados+4  # tamanho da leitura realizada pelo servidor
        self.windowsize = 50

        # instanciando as variaveis de auxilio
        self.arquivo = Arquivo(self.windowsize, self.tamdados)

    def main(self):
        """
        metodo principal do servidor
        :return: so quando o servidor for fechado que esse metodo se incerrara
        """
        # espera da requisicao do cliente
        conexao, cliente = self.tcp.accept()
        pacote = self.waitrequisition(conexao)
        conexao.settimeout(0.1)
        # trata a mensagem do cliente
        tipo, dados, id = Controle.desempacota(pacote)

        # ip porto para envio do video
        clienteudp = literal_eval(dados.decode('utf-8'))

        # espera novamente a requisicao para nome do arquivo
        pacote = self.waitrequisition(conexao)
        tipo, dados, id = Controle.desempacota(pacote)
        dados = 'BigBuckBunny_640x360.m4v'

        # verifica tipo da menssagem
        if tipo == self.GET:    # abrindo o arquivo requisitado pelo cliente
            self.arquivo.obterbitrate(dados)
            #  if self.arquivo.bitrate:
            print('Iniciou transferencia')
            x = self.inittrans(clienteudp, conexao)

    def waitrequisition(self, con):
        """
        Espera da requisicao do cliente
        :return: tupla contendo (ip, porto) do cliente
        """

        pacote=None
        while pacote is None:
            pacote = con.recv(self.bufferread)

        con.send(pacote)  # echo
        return pacote  # requisicao realizada retorno da tupla

    def inittrans(self, cliente, con):
        """
        realiza a transferencia do arquivo mp4 para o cliente
        :return:
        """
        # amarra um porto udp para streamer do video
        self.udp.bind((self.meuip, 0))
        cont = 0
        self.arquivo.abrir() # abrir arquivo para leitura
        sleep(10)
        while True:
            # ler do arquivo tamjanela * tampacotes
            listadados = self.arquivo.leitura()
            if not listadados: # leitura terminada
                break
            # empacota os dados =D
            janela = []
            for dados in listadados:
                janela.append(Controle.empacota(cont, self.TRANS, dados))
                cont += 1
            # envia a janela com os  pacotes e aguarda ack referente a todos
            pacote = self.enviar(janela, cliente, con)

            # controle da identificacao dos pacotes
            if cont == 100:
                cont = 0

            # tratar a mensagem enviada pelo cliente
            tipo, dados, id = Controle.desempacota(pacote)
            while not self.tratartipo(tipo):
                continue

        # refaz ate final do arquivo

        self.arquivo.fechar()   # fim da transferencia
        return True

    def enviar(self, janela, cliente, con):
        """
        Envia os pacotes e espera pelo ack
        timeout -> retransmisao
        :param janela: pacotes
        :return: True fim da transferencia
        """
        flag = True
        pacote=None
        while flag:
            flag = False
            for pacote in janela:
                self.udp.sendto(pacote, cliente)
            try:
                pacote = con.recv(self.bufferread)
            except:     # time error
                flag = True # retransmitir

        return pacote

    def tratartipo(self, tipo):
        """
        trata o tipo da mensagem enviada pelo cliente
        :param tipo: tipo da mensagem
        :return: false quando ack
        """
        if (tipo == self.ACK) or (tipo == self.PLAY):  # continuar transferencia normalmente
            return True
        elif tipo == self.PAUSE:  # parar transferencia ate nova mensagem do cliente
            self.tcp.recv(self.bufferread)
            return False
        elif tipo == self.SEEK:  # avancar uma janela na transferencia
            self.arquivo.avancar()  # avancar a leitura do arquivo
            return True
        elif tipo == self.BACK:  # recua uma janela
            self.arquivo.recuar()   # recuar a leitura do arquivo
            return True

    def fecharconexao(self, con):
        self.udp.close()
        con.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--ip',
        type=str,
        help='Ip do servidor por padrao e usado o ip do myhost'
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        help='Porto TCP do servidor, onde ele recebera a requisicao e '
             'fara os controles'
             'por padrao e 5000'
    )

    args = parser.parse_args()
    porto = 5000
    ip = '127.0.0.1'
    if args.port:
        porto = args.port
    if args.ip:
        ip = args.ip

    s = Servidor((ip, porto))
    s.main()