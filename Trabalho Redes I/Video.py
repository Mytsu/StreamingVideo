from threading import Thread
import os

class Video(Thread):

    def run(self):
        os.system('mpv video')
