'''
YuWei Zhang
V00805647
'''

'''
Adopted from:
- Software Defined Networking (SDN) course by
Professor: Nick Feamster
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel


class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"

    # Hosts
    numberOfHosts = 0
    hosts = []

    # Switches
    coreSwitch = []
    aggregationSwitch = []
    edgeSwtich = []

    def __init__(self, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # self.linkopts1 = linkopts1
        # self.linkopts2 = linkopts2
        # self.linkopts3 = linkopts3
        self.fanout = fanout
        self.numberOfHosts = 4 * self.fanout

        '''
        Create hosts
        '''
        for h in range(1, self.numberOfHosts + 1):
            self.hosts.append(self.addHost('h%s' % h))

        '''
        Add switch
        '''
        # core
        self.coreSwitch.append(self.addSwitch('c1'))

        # aggregation
        for s in range(1, 3):
            self.aggregationSwitch.append(self.addSwitch('a%s' % s))

        # edge
        for s in range(1, 5):
            self.edgeSwtich.append(self.addSwitch('e%s' % s))

        '''
        Create links
        '''
        # linkopt_layer1 = self.linkopts1
        # core -> aggregation
        for i in range(0, 2):
            self.addLink(
                self.coreSwitch[0], self.aggregationSwitch[i])

        # aggregation -> edge
        # linkopt_layekr2 = self.linkopts2
        for i in range(0, 2):
            self.addLink(
                self.aggregationSwitch[0], self.edgeSwtich[i])

        for i in range(2, 4):
            self.addLink(
                self.aggregationSwitch[1], self.edgeSwtich[i])

        # edge -> hosts
        # linkopt_layer3 = self.linkopts3
        for i in range(0, 4):
            for j in range(0, self.fanout):
                self.addLink(
                    self.edgeSwtich[i], self.hosts[i * self.fanout + j])


def perfTest():
    "Create network and run simple performance test"

    # linkopts1 = dict(bw=1000, delay='5ms')
    # linkopts2 = dict(bw=100, delay='8ms')
    # linkopts3 = dict(bw=100, delay='2ms')

    topo = CustomTopo(fanout=2)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth between h1 and h4"
    h1, h4 = net.get('h1', 'h4')
    net.iperf((h1, h4))
    net.stop()



    # Add your logic here ...
if __name__ == '__main__':
    setLogLevel('info')
    perfTest()


topos = {'custom': (lambda: CustomTopo())}
