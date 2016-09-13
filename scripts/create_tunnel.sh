#!/bin/bash

if [ $(whoami) != 'root' ]; then
    echo "Must be root to run $0"
    exit 1;
fi

if [ "$#" -ne 5 ]; then
    echo "Usage: create_tunnel.sh <gre_name> <parent_iface> <local_ip> <remote_ip> <tunnel_ip>"
    exit 0
fi

GRE_NAME=$1
DEV_NAME=$2
LOCAL_IP=$3
REMOTE_IP=$4
TUNNEL_IP=$5

ip tunnel add $GRE_NAME mode gre local $LOCAL_IP remote $REMOTE_IP dev $DEV_NAME
ip addr add $TUNNEL_IP dev $GRE_NAME
ip link set up $GRE_NAME

exit 0

