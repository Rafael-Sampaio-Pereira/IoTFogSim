import pcapy
import bitmath

import tkinter
from twisted.internet import reactor
from twisted.internet import tksupport

from tkinter import *


reader = pcapy.open_offline("fog_received.pcap")

total_packet_size = 0

while True:
    try:
        (header, payload) = reader.next()
        print ("Got a packet of length %d" % header.getlen())
        total_packet_size = total_packet_size+header.getlen()
    except pcapy.PcapError:
        break


total_size = bitmath.Byte(bytes=total_packet_size).best_prefix()

total_size = total_size.format("{value:.2f} {unit}")

print ('Total de pacotes recebidos na Fog: ', total_size)




master = Tk()

master.minsize(width=400, height=400)
w = Label(master, text=total_size)
w.pack()       

mainloop()