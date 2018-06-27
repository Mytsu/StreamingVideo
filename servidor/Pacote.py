class Controle(object):
    """
    Classe para tratar os pacotes e controles como
    envio de pacotes
    empacotar e desempacotar os pacotes
    """

    @staticmethod
    def desempacota(pacote):
        """
        Desempacota separando o cabecalho do corpo
        :param pacote: Bytes lidos do socket
        :return: tipo, dados
        """
        head = pacote[:4]
        id = head[:3]
        tipo = head[3:]
        dados = pacote[4:]

        id = int.from_bytes(id, 'big')
        tipo = int.from_bytes(tipo, 'big')
        return tipo, dados, id

    @staticmethod
    def empacota(id, tipo, dados):
        """
        Empacota os dados para envio
        :param id: id do pacote
        :param tipo: tipo do dados
        :param dados: dados em bytes
        :return: pacote
        """
        id = id.to_bytes(3, 'big')
        tipo = tipo.to_bytes(1, 'big')
        pacote = id + tipo + dados
        return pacote