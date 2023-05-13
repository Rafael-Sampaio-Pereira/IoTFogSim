import numpy as np
import scipy.stats
import random

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



def simulate_network_delay(upper_bound, lower_bound, mean, standard_deviation, global_seed=None, packet_size=None, bandwidth=None):
    """
    this function was based on the below stackoverflow answer, consider that 
    omnet++ inet framework has proved that truncnorm distribution can be used 
    to simulate network delay.
    
    INET documentation example:
    https://github.com/inet-framework/inet/blob/master/examples/internetcloud/cloudandrouters/internetCloud.xml
    
    <internetCloud symmetric="true">
        <parameters name="good">
            <traffic src="srouter[0]" dest="rrouter" delay="20ms+truncnormal(200ms,60ms)" datarate="uniform(100kbps,1Mbps)" drop="uniform(0,1) &lt; 0.01" />
            <traffic src="srouter[1]" dest="rrouter" delay="30ms+truncnormal(200ms,60ms)" datarate="uniform(100kbps,1Mbps)" drop="uniform(0,1) &lt; 0.02" />
            <traffic src="srouter[2]" dest="rrouter" delay="40ms+truncnormal(200ms,60ms)" datarate="uniform(100kbps,1Mbps)" drop="uniform(0,1) &lt; 0.03" />
            <traffic src="srouter[3]" dest="rrouter" delay="50ms+truncnormal(200ms,60ms)" datarate="uniform(100kbps,1Mbps)" drop="uniform(0,1) &lt; 0.04" />
            <traffic src="srouter[4]" dest="rrouter" delay="60ms+truncnormal(200ms,60ms)" datarate="uniform(100kbps,1Mbps)" drop="uniform(0,1) &lt; 0.05" />
            <traffic src="srouter[5]" dest="rrouter" delay="70ms+truncnormal(200ms,60ms)" datarate="uniform(100kbps,1Mbps)" drop="uniform(0,1) &lt; 0.06" />
            <traffic src="srouter[6]" dest="rrouter" delay="80ms+truncnormal(200ms,60ms)" datarate="uniform(100kbps,1Mbps)" drop="uniform(0,1) &lt; 0.07" />
            <traffic src="srouter[7]" dest="rrouter" delay="90ms+truncnormal(200ms,60ms)" datarate="uniform(100kbps,1Mbps)" drop="uniform(0,1) &lt; 0.08" />
            <traffic src="srouter[8]" dest="rrouter" delay="100ms+truncnormal(200ms,60ms)" datarate="uniform(100kbps,1Mbps)" drop="uniform(0,1) &lt; 0.09" />
            <traffic src="srouter[9]" dest="rrouter" delay="110ms+truncnormal(200ms,60ms)" datarate="uniform(100kbps,1Mbps)" drop="uniform(0,1) &lt; 0.10" />
            <!--
                <traffic src="**" dest="**" delay="10ms+truncnormal(100ms,20ms)" datarate="uniform(100kbps,500kbps)" drop="uniform(0,1) &lt; uniform(0.01, 0.05)" />
            -->
        </parameters>
    </internetCloud>
    
    https://stackoverflow.com/a/28013759
    I came across this post while searching for a way to return a series of 
    values sampled from a normal distribution truncated between zero and 1 
    (i.e. probabilities). To help anyone else who has the same problem, I just
    wanted to note that scipy.stats.truncnorm has the built-in capability ".rvs".
    So, if you wanted 100,000 samples with a mean of 0.5 and standard deviation of 0.1:
    
    import scipy.stats
    lower = 0
    upper = 1
    mu = 0.5
    sigma = 0.1
    N = 100000

    samples = scipy.stats.truncnorm.rvs(
            (lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=N)
    
    This gives a behavior very similar to numpy.random.normal, but within the
    bounds desired. Using the built-in will be substantially faster than
    looping to gather samples, especially for large values of N.
    
    usage example:
        delay = simulate_network_delay(200, 60, 70, 10)
    
    """
    if global_seed:
        random.seed(global_seed)
    
    mu = mean
    sigma = standard_deviation
    N = 100000 # number of samples
    samples = scipy.stats.truncnorm.rvs(
            (lower_bound-mu)/sigma,(upper_bound-mu)/sigma,loc=mu,scale=sigma,size=N)

    sample = random.choice(samples)
    delay = float(round((sample/1000),3))
    if bandwidth and packet_size:
        # Adds bandwidth delay to the network latency randomiclly generated
        delay += packet_size/bandwidth
    return delay