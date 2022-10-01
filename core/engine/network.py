import numpy as np


def extract_ip_prefix(ip):
    l = ip.split('.')
    return f"{l[0]}.{l[1]}.{l[2]}"

def drop_packet(loss_rate: float, global_seed) -> bool:
    """
    IoTFogSim Packet Loss Module
    Author: Rafael Sampaio
    Date: 01 May 2022

    This function is a probabilistic function that indicates chances of a packet be lose 

    This function is inspired in a stack overflow answer avaliable at:
    https://stackoverflow.com/questions/43017074/simulate-packet-loss-in-udp-in-python

    Simulate packet loss in UDP in python

    Question:
    I am supposed to simulate a packet loss rate of 10^-2 in a Stop-and-wait protocol,
    that is 0.01, which means that 1 out of 100 packets transmitted get lost. Suppose
    I'm sending 1000 packets, how to drop exactly 1 random packet out of the 100 packets
    sent throughout the transmission ? - Jarvis

    Answer:
    Having a rate of 0.01 doesn't mean that exactly 1 out of 100 packets gets dropped.
    It means that each packet has a 1% chance of getting lost. Under the assumption that
    losses are independent of each other, the actual number of lost packets will follow
    a binomial distribution.

    For each packet you generate, check if a random Uniform(0,1) is less than or equal to
    the proportion of losses p, in your case 0.01. If it is, that packet is lost,
    otherwise it goes through. This approach scales if you increase or decrease the N, the
    total number of packets. The expected number of losses will be N * p, but if you
    repeat the experiment multiple times there will be variability. - pjs

    Parameters:
        loss-rate: float < 1 | Percentual chance of packet be lose
    Return:
        bool: Boolean that indicates if current packet can or can not be dropped.

    Usage:
        res = drop_packet(0.05)
        if res:
            do your drop code here
    """
    
    if global_seed:
        np.random.seed(global_seed)
    # Indicates the total chance of a given packet be dropped. For 1 of 100 packets use 1/100, so rate is 0.01
    rand_value = np.random.uniform(0, 1)
    if rand_value <= loss_rate:
        return True
    return False
