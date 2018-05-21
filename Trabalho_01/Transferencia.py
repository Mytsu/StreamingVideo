from threading import Thread
import socket
import os
import select


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
        # o nome esta em formato de bytes entao foi decodificado para transforma-lo em uma string
        self.nome = self.nome.decode()
        arquivo = self.nome.split(" ")
        # diretorio streamer mais o nome do arquivo digitado
        diretorio = (os.path.dirname(os.path.realpath(__file__))) + "/streamer/" + arquivo[1]

        try:
            self.arq = open(diretorio, "rb") # leitura em forma de bytes
        except FileNotFoundError:
            return 0             # arquivo nao encontrado

        return arquivo[1]                       # se ok return nome do arquivo

    def run(self):
        """
        Transferencia do arquivo
        :return:
        """
        if self.arquivo == 0:
            return -1                         # enviar menssagem de erro ao cliente

        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        contamsg = 0
        tamanho_msg = int(1).to_bytes(1, 'big')
        while int.from_bytes(tamanho_msg, 'big') != 0:
            msg = self.arq.read(self.buffleitura)  # leitura de n bits do arquivo
            tamanho_msg = len(msg).to_bytes(2, 'big')
            contamsg = contamsg.to_bytes(2, 'big')
            head = b''.join([contamsg, tamanho_msg])
            msg = b''.join([head, msg])
            udp.sendto(msg, self.dest)
            sock = udp.getsockname()
            ready_to_read, ready_to_write, in_error = select.select(
                    [sock[1]],
                    [sock[1]],
                    []
            )
            if ready_to_read != None :
                print('oi')
        udp.close()


