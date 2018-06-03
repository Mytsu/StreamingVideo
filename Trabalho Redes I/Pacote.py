class Pacote(object):
    def __init__(self, dados, ack, timeout):
        self.dados = dados
        self.ack = ack
        self.time = timeout
