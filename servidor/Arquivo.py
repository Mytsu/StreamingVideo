import subprocess

class Arquivo(object):
    """
    Classe para tratar os diversos tipos de leitura para o
    arquivo requisitado
    """
    def __init__(self, tamjanela, tamdados):
        self.__nome = None
        self.__rate = None
        self.__arquivo = None
        self.__tamjanela = tamjanela
        self.__tamdados = tamdados

    def obterbitrate(self, nomedoarquivo):
        """
        Obtem o bitrate do arquivo mpv requerido
        :param nomedoarquivo: nome do arquivo mpv
        :return: bitrate do arquivo
        """

        # usa mediainfo para coletar o bitrate do video
        bitrate = subprocess.Popen(["mediainfo", "--Output='Video;%BitRate%;'", self.__nome], stdout=subprocess.PIPE).communicate()[0]

        # verifica a existencia do arquivo

        # verifica se arquivo e do formato mp4

        # leitura do bitrate do arquivo

        # fecha arquivo
        self.__nome = nomedoarquivo
        self.__rate = bitrate

    def abrir(self):
        """
        Abrir o arquivo para iniciar a transferencia
        :return:
        """
        self.__arquivo = open(self.__nome, "rb")  # ler bytes do arquivo

    def fechar(self):
        """
        Fechar o arquivo ao final da transferencia
        :return:
        """
        self.__arquivo.close()

    def leitura(self):
        """
        leitura do arquivo para envio para o cliente
        :param size: tamanho da janela * tamdados
        :return: lista com dados lidos
        """
        listadados = []
        for i in range(self.__tamjanela):
            read = self.__arquivo.read(self.__tamdados)
            listadados.append(read)

        return listadados

    def recuar(self):
        self.__arquivo.seek(-self.__tamjanela*self.__tamdados, 1)

    def avancar(self):
        self.__arquivo.seek(self.__tamjanela * self.__tamdados, 1)

    @property
    def nome(self):
        return self.__nome

    @property
    def bitrate(self):
        return self.__rate