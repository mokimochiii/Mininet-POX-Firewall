#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import RemoteController
class MyTopology(Topo):
    """
    A basic topology
    """
    def __init__(self):
        Topo.__init__(self)
        # Set Up Topology Here
        switch1 = self.addSwitch('s1') ## Adds a Switch
        switch2 = self.addSwitch('s2')
        iPad = self.addHost('ipad', ip='10.1.1.1') ## Adds a Host
        self.addLink(switch1, iPad, delay='20ms') ## Add a link
        Laptop = self.addHost('laptop', ip='10.1.1.2') ## Adds a Host
        self.addLink(switch1, Laptop, delay='20ms')
        Webserver = self.addHost('webserver', ip='10.1.1.3')
        self.addLink(switch1, Webserver, delay='20ms')
        Lights = self.addHost('lights', ip='10.1.20.1')
        self.addLink(switch2, Lights, delay='20ms')
        Heater = self.addHost('heater', ip='10.1.20.2')
        self.addLink(switch2, Heater, delay='20ms')
        self.addLink(switch1, switch2, delay='20ms')
if __name__ == '__main__':
    """
    If this script is run as an executable (by chmod +x), this is
    what it will do
    """
    topo = MyTopology() ## Creates the topology
    c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    net = Mininet(topo=topo, controller=c0) ## Loads the topology
    net.start() ## Starts Mininet
    # Commands here will run on the simulated topology
    CLI(net)
    net.stop()
