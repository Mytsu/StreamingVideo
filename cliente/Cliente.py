import socket
import argparse
from Pacote import Controle
from Fragmento import Fragmento
import sys


class Cliente(object):
    """
    Parte do cliente fazer a requisicao do video
    executar o video
    ---pausar
    ---seek
    ---back
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

    def __init__(self, meuip, ip_porto_servidor, arquivo):
        """

        :param meuip: Ip do cliente
        :param ip_porto_servidor: tupla com (ip, porto) do servidor para requisicao
        :param arquivo: inteiro identificando qual arquivo a ser requisitado
        """

        # instanciando as variaveis de conexao de TCP e UDP
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # instanciando variaveis para guardar o ip porto do servidor de requisicao
        self.servidor = ip_porto_servidor

        # salvando meuip e arquivo de video a ser requisitado para stream
        self.meuip = meuip
        self.arquivo = arquivo

        # variaveis de controle
        self.tamdados = 1020  # bytes de dados dentro do pacote
        self.bufferread = self.tamdados + 4  # tamanho da leitura realizada pelo servidor
        self.windowsize = 50

    def main(self):
        """
        Funcao princial
        :return:
        """

        # estabelecer conexao tcp com o servidor para controle
        if not self.conectar():
            pass
        print('conexao estabelecida')
        # requisita arquivo
        if not self.requisita():
            pass

        # iniciar stream de video
        self.streamer()

        self.tcp.close()

    def conectar(self):
        """
        Estabelece conexao com o servidor
        :return:
        """
        self.tcp.connect(self.servidor)
        # amarrando porta udp aleatoria
        self.udp.bind((self.meuip, 0))
        pacote = Controle.empacota(0, self.GET, str(self.udp.getsockname()).encode('utf-8'))
        # enviando a porta udp para o servidor

        self.tcp.send(pacote)
        self.tcp.recv(self.bufferread)  # aguardando echo

        return True

    def requisita(self):
        """
        Requisita o video ao servidor
        :return:
        """
        arquivo = self.arquivo.to_bytes(self.tamdados, 'big')
        pacote = Controle.empacota(0, self.GET, arquivo)
        self.tcp.send(pacote)
        self.tcp.recv(self.bufferread)  # aguardando echo
        return True

    def streamer(self):
        """

        :return:
        """
        while True:
            # receber janela
            janela = []
            while len(janela) < self.windowsize:
                pacote = self.udp.recv(self.bufferread)
                tipo, dados, id = Controle.desempacota(pacote)
                frag = Fragmento(tipo, dados, id)
                if frag not in janela:
                    janela.append(frag)

            janela.sort(key=lambda x: x.id)
            # enviar ack
            self.tcp.send(Controle.empacota(0, self.ACK, b'\x00'))
            # salvar no buffer de saida
            for item in janela:
                sys.stdout.buffer.write(item.dados)
            # verificar interrupcao do teclado

            # tratar interrupcao

        # repetir ate final do video
    def receber(self):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--ip',
        type=str,
        help='Ip do servidor por padrao e usado o ip do myhost'
    )
    parser.add_argument(
        '-m',
        '--meuip',
        type=str,
        help='Seu ip na rede local'
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        help='Porto TCP do servidor no formato inteiro'
    )

    parser.add_argument(
        'video_requisicao',
        type=int,
        help='Inteiro informando o arquivo desejado'
    )

    args = parser.parse_args()
    porto = 5000
    ip = '127.0.0.1'
    arquivo = args.video_requisicao
    meuip = '127.0.0.1'
    if args.port:
        porto = args.port
    if args.ip:
        ip = args.ip
    if args.meuip:
        meuip = args.meuip

    c = Cliente(meuip, (ip, porto), arquivo)
    c.main()
