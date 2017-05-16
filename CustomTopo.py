
'''
YuWei Zhang
V00805647
'''

'''
Adopted from:
- Software Defined Networking (SDN) course by
Professor: Nick Feamster
'''

#!/usr/bin/python

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

    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        self.linkopts1 = linkopts1
        self.linkopts2 = linkopts2
        self.linkopts3 = linkopts3
        self.fanout = fanout
        self.numberOfHosts = 4 * self.fanout

        core = self.addSwitch('c1')

        aggregation1 = self.addSwitch('a1')
        aggregation2 = self.addSwitch('a2')

        edge1 = self.addSwitch('e1')
        edge2 = self.addSwitch('e2')
        edge3 = self.addSwitch('e3')
        edge4 = self.addSwitch('e4')

        self.addLink(core, aggregation1, **linkopts1)
        self.addLink(core, aggregation2, **linkopts1)

        self.addLink(aggregation1, edge1, **linkopts2)
        self.addLink(aggregation1, edge2, **linkopts2)
        self.addLink(aggregation2, edge3, **linkopts2)
        self.addLink(aggregation2, edge4, **linkopts2)

        '''
        Create hosts
        '''
        for i in irange(1, self.numberOfHosts):
            host = self.addHost('h%s' % i)

            if i <= fanout * 1:
                self.addLink(host, edge1, **linkopts3)
            elif i > fanout * 1 and i <= fanout * 2:
                self.addLink(host, edge2, **linkopts3)
            elif i > fanout * 2 and i <= fanout * 3:
                self.addLink(host, edge3, **linkopts3)
            else:
                self.addLink(host, edge4, **linkopts3)


def getLinkConfig(message):
    while True:
        try:
            linkoption_input = raw_input(message).split()
            linkopts = dict(
                bw=float(linkoption_input[0]), delay=linkoption_input[1] + "ms")
            return linkopts
        except:
            print "Error: Integer only ! Example input: => 100 1"


def perfTest():
    "Create network and run simple performance test"

    "Number of hosts"
    numHosts = raw_input(
        "Please enter the number of child per node\n => ")
    numHosts = int(numHosts)

    "Get network options"
    linkopts1 = getLinkConfig("Please enter bandwidth and delay for linkoption1 (core -> aggregation) separated by space\n => ")
    linkopts2 = getLinkConfig("\nPlease enter bandwidth and delay for linkoption1 (aggregation -> edge) separated by space\n => ")
    linkopts3 = getLinkConfig("\nPlease enter bandwidth and delay for linkoption1 (edge -> host) separated by space\n => ")

    print "\nFanout is " + str(numHosts)
    print "\nCore -----> Aggregation: bw=" + str(linkopts1['bw']) + ", delay=" + str(linkopts1['delay']) + "ms"
    print "\nAggregation -----> Edge: bw=" + str(linkopts2['bw']) + ", delay=" + str(linkopts2['delay']) + "ms"
    print "\nEdge -----> Host: bw=" + str(linkopts3['bw']) + ", delay=" + str(linkopts3['delay']) + "ms"

    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=int(numHosts))
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
