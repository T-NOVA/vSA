#!/bin/bash
for i in 1 2 5 10 20 50 100
#for i in 20 50 100
do
	echo "##################################"
	echo "Verbindungen $i"
	sudo tcpdump -qti eth0 -w pfsense-test.pcap & iperf -c 192.168.1.2 -t 100 -P $i
	#sleep 120
	sudo killall tcpdump
	sudo tcptrace -xtraffic pfsense-test.pcap
	cat traffic_stats.dat
	if [ $i -eq 2 ]; then
		echo "##################################"
		echo "Verbindungen $i dual"
		sudo tcpdump -qti eth0 -w pfsense-test.pcap & iperf -c 192.168.1.2 -t 100 -P $i -d
	#	sleep 120
		sudo killall tcpdump
		sudo tcptrace -xtraffic pfsense-test.pcap
		cat traffic_stats.dat
	fi
done

