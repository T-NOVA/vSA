#!/bin/bash

# eth0 aktivieren
ip addr add 192.168.3.2/24 broadcast 192.168.3.255 dev eth0
ip link set eth0 up

# Namensschema einstellen (vlanX)
vconfig set_name_type VLAN_PLUS_VID_NO_PAD

# VLAN-Interfaces anlegen
vconfig add eth0 1
vconfig add eth0 2

# VLAN-Interfaces konfigurieren und aktivieren
ip addr add 192.168.4.2/24 broadcast 192.168.4.255 dev vlan1
ip link set vlan1 up
ip addr add 192.168.5.2/24 broadcast 192.168.5.255 dev vlan2
ip link set vlan2 up

ifconfig
