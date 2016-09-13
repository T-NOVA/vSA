#!/bin/bash

IFACES=(tap0 tap1 tap2)
PORTS=()
bridge="br0"
mirror_name="snortmirror"

if [ $(whoami) != 'root' ]; then
    echo "Must be root to run $0"
    exit 1;
fi

echo -e "\
    -----------------\n\
    Creating bridge \"$bridge\":\n\
      phys. interfaces: ${IFACES[*]}\n\
                mirror: $mirror_name\n\
    -----------------"

# create bridge
ovs-vsctl add-br "$bridge"

for iface in ${IFACES[*]}; do
    # remove any ip addresses from interface
    ip addr flush dev "$iface"
    # set interface down
    ip link set down dev "$iface"
    ovs-vsctl add-port "$bridge" "$iface"
    port="$(sudo ovs-vsctl get port "$iface" _uuid)"
    PORTS+=($port)
done

echo "${PORTS[*]}"

# specific setup

# setup mirror
# mirroring traffic from tap0 to tap1
ovs-vsctl -- --id=@m create mirror name=$mirror_name -- add bridge $bridge mirrors @m
ovs-vsctl set mirror $mirror_name select_src_port=${PORTS[0]} select_dst_port=${PORTS[0]}
ovs-vsctl set mirror $mirror_name output-port=${PORTS[1]}

for iface in ${IFACES[*]}; do
    ip link set up dev "$iface"
done

exit 0;
