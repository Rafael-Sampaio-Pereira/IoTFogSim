import pcapy
import bitmath

import tkinter
from twisted.internet import reactor
from twisted.internet import tksupport

from tkinter import *
from twisted.internet.task import LoopingCall


def get_total_size_from_pcap_file(file_path, label):
    reader = pcapy.open_offline(file_path)
    total_packet_size = 0

    while True:
        try:
            (header, payload) = reader.next()
            total_packet_size = total_packet_size+header.getlen()
            print(payload)
        except pcapy.PcapError:
            break
    total_size = bitmath.Byte(bytes=total_packet_size).best_prefix().format("{value:.2f} {unit}")

    print ('Total size of received data: ', total_size)
    label.config(text="Total size of received data: "+str(total_size))
    return total_size


def main():

    master = Tk()
    tksupport.install(master)
    master.title("Network Packets Monitoring - V.0.1")
    master.minsize(width=400, height=400)
    total_label = Label(master, text="Total size of received data: "+str(0))
    total_label.pack()

    loop_for_read_new_data = LoopingCall(get_total_size_from_pcap_file, file_path="fog_received.pcap", label=total_label)
    loop_for_read_new_data.start(30) # updating every 30 seconds

# mainloop()


if __name__ == '__main__':
    main()
    reactor.run()

