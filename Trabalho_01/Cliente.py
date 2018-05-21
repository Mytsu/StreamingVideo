import socket


class Cliente(object):

    def __init__(self, porto = 12000):
        self.meuip = socket.gethostbyname(socket.gethostname())
        self.porta_servidor = 5000
        self.endereco_servidor = '10.120.7.45'
        self.porto_recebimento = porto
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = (self.endereco_servidor, self.porta_servidor)
        orig = (self.meuip, self.porto_recebimento)
        self.udp.bind(orig) # requerindo a amarracao da porta de recebimento

    def requerimento_servidor(self):
        ba = bytearray()
        while True:
            msg = "arquivos lista" # envio uma menssagem de conexao com o servidor para ele informar os arquivos
            self.udp.sendto(msg.encode("utf-8"), self.dest)
            response = self.udp.recv(2048)
            while response != 'encerramento_lista'.encode('utf-8'):
                print(response.decode())
                response = self.udp.recv(2048)

            msg = input("Informe o arquivo desejado: (Get 'Arquivo')")
            self.udp.sendto(msg.encode("utf-8"), self.dest)

            response = 'passar'.encode("utf-8")
            arq = open("novo", "wb")
            while response != b'':
                response, porto_transferencia = self.udp.recv(2048)
                head = ba.join([response])
                # head 0 - 4 -> 0 - 2 : Id msg e 2 - 4 : tamanho da msg
                contmsg = head[0:2]
                tamanho = head[2:4]
                msg = b'\x01'
                msg = ba.join([msg, contmsg])
                self.udp.sendto(msg, porto_transferencia)


                arq.write(response)
            break

    def encerramento(self):
        self.udp.close()

if __name__ == '__main__':
    cliente = Cliente()
    cliente.requerimento_servidor()