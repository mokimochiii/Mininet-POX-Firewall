## USAGE
ONLY RUN THESE FILES IN MININET
Save topo.py in the root directory
Save controller.py in ~/pox/pox/misc
Start the topology with:
```bash
  sudo python topo.py
```
Start the controller with:
```bash
  sudo ~pox/pox.py log.level --packet=WARN misc.controller
```

## FIREWALL RULES
General Connectivity: To facilitate general network connectivity, allow all ARP traffic across the network

DoS Protection: Allow all ICMP traffic across the network EXCEPT those sent to the Web Server

Web Traffic: Allow all TCP traffic between the laptop and the iPad.  

IoT devices: Allow all UDP  traffic between the heater and the lights.  Allow all TCP traffic between the iPad and the IoT devices (heater and lights). 

Laptop/iPad General Management: Allow all UDP traffic between the laptop and the iPad.

Default Deny: Block all traffic that does not match the above criteria.
