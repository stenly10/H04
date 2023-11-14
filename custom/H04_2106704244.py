"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
from mininet.node import Node

class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')
    
    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class MyTopo( Topo ):
    def build( self ):

        default_gateway_koas = '192.168.244.1/26'
        default_gateway_internship = '192.168.244.65/27'
        default_gateway_spesialis = '192.168.244.97/28'
        default_gateway_residen = '192.168.244.113/29'

        router_asrama = self.addNode('r0', cls=LinuxRouter, ip=default_gateway_koas)
        router_rs = self.addNode('r1', cls=LinuxRouter, ip=default_gateway_spesialis)
        
        asrama_rs = '192.168.244.121/30'
        rs_asrama = '192.168.244.122/30'
        
        switch_k = self.addSwitch('s1')
        switch_i = self.addSwitch('s2')
        switch_s = self.addSwitch('s3')
        switch_r = self.addSwitch('s4')

        self.addLink(switch_k, router_asrama, intfName2='r0-eth1', params2={'ip':default_gateway_koas})
        self.addLink(switch_i, router_asrama, intfName2='r0-eth2', params2={'ip':default_gateway_internship})
        self.addLink(switch_s, router_rs, intfName2='r1-eth1', params2={'ip':default_gateway_spesialis})
        self.addLink(switch_r, router_rs, intfName2='r1-eth2', params2={'ip':default_gateway_residen})
        self.addLink(router_asrama, router_rs, intfName1 = 'r0-eth3', intfName2='r1-eth3', params1={'ip':asrama_rs}, params2={'ip':rs_asrama})

        for switch in ['s1', 's2', 's3', 's4']:
            if switch == 's1':
                for j in range(61):
                    host_name = f'K{j+1}'
                    ip_addr = f'192.168.244.{j+2}/26'
                    self.addHost(host_name, ip=ip_addr, defaultRoute=f'via {default_gateway_koas[:-3]}')
                    self.addLink(host_name, switch)
            elif switch == 's2':
                for j in range(29):
                    host_name = f'I{j+1}'
                    ip_addr = f'192.168.244.{j+66}/27'
                    self.addHost(host_name, ip=ip_addr, defaultRoute=f'via {default_gateway_internship[:-3]}')
                    self.addLink(host_name, switch)
            elif switch == 's3':
                for j in range(13):
                    host_name = f'S{j+1}'
                    ip_addr = f'192.168.244.{j+98}/28'
                    self.addHost(host_name, ip=ip_addr, defaultRoute=f'via {default_gateway_spesialis[:-3]}')
                    self.addLink(host_name, switch)
            else:
                for j in range(5):
                    host_name = f'R{j+1}'
                    ip_addr = f'192.168.244.{j+114}/28'
                    self.addHost(host_name, ip=ip_addr, defaultRoute=f'via {default_gateway_residen[:-3]}')
                    self.addLink(host_name, switch)
            
topos = { 'mytopo': ( lambda: MyTopo() ) }
