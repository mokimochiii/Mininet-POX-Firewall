from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
    def __init__ (self, connection):
        self.connection = connection
        connection.addListeners(self)

    def do_firewall (self, packet, packet_in):
        def accept():
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.data = packet_in
            msg.idle_timeout = 60
            msg.hard_timeout = 300
            msg.actions.append(of.ofp_action_output(port=of.OFPP_NORMAL))
            msg.buffer_id = packet_in.buffer_id
            self.connection.send(msg)
            print(f"Packet Accepted - Flow Table Installed on Switches")


        def drop ():
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet, packet_in.in_port)
            msg.buffer_id = packet_in.buffer_id
            msg.in_port = packet_in.in_port
            self.connection.send(msg)
            print(f"Packet Dropped - Flow Table Installed on Switches")
        
        ipv4 = packet.find('ipv4')
        arp = packet.find('arp')
        icmp = packet.find('icmp')
        tcp = packet.find('tcp')
        udp = packet.find('udp')

        #print("Rule 1")
        #Rule 1:
        #allow all arp packets
        if arp:
            accept()
            return
    
        #allow all icmp packets
        if icmp:
            #except those going to webserver
            if ipv4.dstip == '10.1.1.3':
                drop()
                return
            accept()
            return
        
        #print("Rule 2")
        #Rule 2:
        #allow all TCP traffic between laptop and ipad
        if ipv4 and tcp:
            src = ipv4.srcip
            dst = ipv4.dstip
            if (src == '10.1.1.1' and dst == '10.1.1.2') or (src == '10.1.1.2' and dst == '10.1.1.1'):
                accept()
                return
            
        #print("Rule 3")
        #Rule 3:
        #Allow all TCP traffic between iPad and IoT devices
        if ipv4 and tcp:
            src = ipv4.srcip
            dst = ipv4.dstip
            if (src == '10.1.1.1' and dst == '10.1.20.1') or (src == '10.1.20.1' and dst == '10.1.1.1'):
                accept()
                return
            
            if (src == '10.1.20.2' and dst == '10.1.1.1') or (src == '10.1.1.1' and dst == '10.1.20.2'):
                accept()
                return

        #Allow all UDP traffic between the heater and lights
        if ipv4 and udp:
            src = ipv4.srcip
            dst = ipv4.dstip
            if src == '10.1.20.2' and dst == '10.1.20.1':
                accept()
                return
            if src == '10.1.20.1' and dst == '10.1.20.2':
                accept()
                return
            
        #print("Rule 4")
        #Rule 4:
        #Allow all UDP traffic between the laptop and the ipad
        if ipv4 and udp:
            src = ipv4.srcip
            dst = ipv4.dstip
            if src == '10.1.1.2' and dst == '10.1.1.1':
                accept()
                return
            
        #print("Rule 5")
        #Rule 5:
        #Block all traffic that does not meet the above criteria
        drop()

    def _handle_PacketIn (self, event):
        packet = event.parsed
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return
        packet_in = event.ofp
        self.do_firewall(packet, packet_in)

def launch ():
    def start_switch (event):
        log.debug("Controlling %s" % (event.connection,))
        Firewall(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
