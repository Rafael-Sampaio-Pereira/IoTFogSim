from twisted.internet import reactor
from twisted.python import log
import sys
import tkinter
from tkinter import PhotoImage

import PIL
from PIL import ImageTk, Image
import random

from core.configurations import CoreConfig

from threading import Thread

import sys
sys.dont_write_bytecode = True

import subprocess

# def suspend_screensaver():
#     window_id = subprocess.Popen('xwininfo -root | grep xwininfo | cut -d" " -f4', stdout=subprocess.PIPE, shell=True).stdout.read().strip()

#     #run xdg-screensaver on root window
#     subprocess.call(['xdg-screensaver', 'suspend', window_id])

# def resume_screensaver(window_id):
#     subprocess.Popen('xdg-screensaver resume ' + window_id, shell=True)




if __name__ == '__main__':
    from multiprocessing import Process
    
    CoreConfig()
    proc2 = Process(target=reactor.run)
    proc2.start()



