from threading import Thread
import os
from time import sleep


class Video(Thread):

    def run(self):
        sleep(2)
        os.system('mpv  video ')
