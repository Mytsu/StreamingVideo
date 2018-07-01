import sys
from time import sleep
from threading import Thread

class Consumidor(Thread):
    def __init__(self, lock, bitrate):
        Thread.__init__(self)
        self.lista = []
        self.lock = lock
        self.rate = bitrate

    def run(self):

        while True:
            sleep(0.003)

            if not self.lista:
                continue
            else:
                self.removelista()

    def addlista(self, pacote):
        self.lock.acquire()
        self.lista.append(pacote)
        self.lock.release()

    def removelista(self):
        self.lock.acquire()
        pacote = self.lista.pop(0)
        self.lock.release()

        #print(pacote.dados)
        sys.stdout.buffer.write(pacote.dados)
