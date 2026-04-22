from mininet.topo import Topo

class SimpleTopo(Topo):
    def build(self):
        # Create switch
        s1 = self.addSwitch('s1')

        # Create hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)


topos = {'simpletopo': (lambda: SimpleTopo())}

# To show the flows in the switch s1.

# mininet> sh ovs-ofctl dump-flows s1