#!/bin/sh
iface=$1
num=$2
echo "Creating $num blocking rules for interface $iface..."
for i in $( jot $num 1 $num );
do
	echo $i
	ip=`jot -r 4 1 255`
	ip=`echo $ip | tr ' ' '.'`
	easyrule block $iface $ip
done
echo "...done."

