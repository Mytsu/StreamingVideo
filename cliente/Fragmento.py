class Fragmento(object):
    """
    Classe que contem cada fragmento do video separado em objetos
    """
    def __init__(self, tipo, dados, id):
        self.__id = id
        self.__dados = dados


    @property
    def id(self):
        return self.__id

    @property
    def dados(self):
        return self.__dados

    def __eq__(self, other):
        return self.id == other.id
