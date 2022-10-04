# from twisted.internet.defer import inlineCallbacks
# from twisted.internet import reactor
# from twisted.internet.task import deferLater


# def sleep(secs):
#     return deferLater(reactor, secs, lambda: None)


# @inlineCallbacks
# def f():
#     print('writing for 5 seconds ...')
#     yield sleep(0.5)
#     print('now i am back ...')

import scipy.stats
import random

def simulate_network_delay(upper_bound, lower_bound, mean, standard_deviation, global_seed=None):
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
    delay = round((sample/1000),3)
    return delay
        
        
print(simulate_network_delay(200, 60, 70, 10))


