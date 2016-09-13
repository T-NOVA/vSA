#!/bin/vbash
#create firewall rules for vyos
source opt/vyatta/etc/functions/script-template
iface=1
num=5
echo "Creating $num blocking rules for interface $iface"
delete firewall name BLOCKED-IPS
for i in $(seq 1 $num)
do
	echo $i
	ip=$(shuf -i4-255 -n4)
	ip=$(echo $ip | tr ' ' '.')
	echo $ip
	configure
	set firewall name BLOCKED-IPS rule $i action drop
	set firewall name BLOCKED-IPS rule $i source address $ip
done
set interfaces ethernet eth$iface firewall in name 'BLOCKED-IPS'
show firewall
commit
save
exit
echo "Done!"
