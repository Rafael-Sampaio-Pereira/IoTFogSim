from twisted.internet import reactor
from twisted.python import log
import sys
import tkinter
from tkinter import PhotoImage

import PIL
from PIL import ImageTk, Image
import random

from scinetsim.configurations import config
from scinetsim.configurations import  load_nodes

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


def main():
    # suspend_screensaver()
    config()


if __name__ == '__main__':
    main()
    reactor.run()

