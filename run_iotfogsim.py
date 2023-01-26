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


if __name__ == '__main__':
    CoreConfig()
    reactor.run()



