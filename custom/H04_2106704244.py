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
        num_switch = 5
        number_host_per_switch_1 = 6
        number_host_per_switch_2 = 5

        default_gateway_koas = '192.168.244.1/26'
        default_gateway_internship = '192.168.244.65/27'
        default_gateway_spesialis = '192.168.244.97/28'
        default_gateway_residen = '192.168.244.113/29'

        router_asrama = self.addNode('Router Asrama', cls=LinuxRouter, ip=default_gateway_koas)
        router_rs = self.addNode('Router RS', cls=LinuxRouter, ip=default_gateway_spesialis)

        switch_k = self.addSwitch('Switch_K')
        switch_i = self.addSwitch('Switch_I')
        switch_s = self.addSwitch('Switch_S')
        switch_r = self.addSwitch('Switch_R')

        self.addLink(switch_k, router_rs, intfName2='router_asrama-eth1', params2={'ip':default_gateway_koas})
        self.addLink(switch_i, router_rs, intfName2='router_asrama-eth2', params2={'ip':default_gateway_internship})
        self.addLink(switch_s, router_asrama, intfName2='router_rs-eth1', params2={'ip':default_gateway_spesialis})
        self.addLink(switch_r, router_asrama, intfName2='router_rs-eth2', params2={'ip':default_gateway_residen})
        # self.addLink(router_asrama, router_rs)

        for switch in ['Switch_K', 'Switch_I', 'Switch_S', 'Switch_R']:
            if switch == 'Switch_K':
                for j in range(number_host_per_switch_1):
                    host_name = f'K{j+1}'
                    ip_addr = f'192.168.244.{j+2}/26'
                    self.addHost(host_name, ip=ip_addr, defaultRoute=f'via {default_gateway_koas}')
                    self.addLink(host_name, switch)
            elif switch == 'Switch_I':
                for j in range(number_host_per_switch_1):
                    host_name = f'I{j+1}'
                    ip_addr = f'192.168.244.{j+66}/27'
                    self.addHost(host_name, ip=ip_addr, defaultRoute=f'via {default_gateway_internship}')
                    self.addLink(host_name, switch)
            elif switch == 'Switch_S':
                for j in range(number_host_per_switch_1):
                    host_name = f'S{j+1}'
                    ip_addr = f'192.168.244.{j+98}/28'
                    self.addHost(host_name, ip=ip_addr, defaultRoute=f'via {default_gateway_spesialis}')
                    self.addLink(host_name, switch)
            else:
                for j in range(number_host_per_switch_2):
                    host_name = f'R{j+1}'
                    ip_addr = f'192.168.244.{j+114}/28'
                    self.addHost(host_name, ip=ip_addr, defaultRoute=f'via {default_gateway_residen}')
                    self.addLink(host_name, switch)
            
topos = { 'mytopo': ( lambda: MyTopo() ) }
