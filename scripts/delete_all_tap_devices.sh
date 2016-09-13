#!/bin/bash

BASE_NAME="tap"

# check if root
if [ `whoami` != "root" ]; then
	echo "Must be run as root!"
	exit 1
fi

ARGS=1

if [ $# -ne "$ARGS" ]; then
  echo "Usage: $0 <index of last device to delete>"
  exit $E_BADARGS
fi

echo "Deleting $(($1+1)) tap devices.."

for t in $(seq 0 $1); do
	echo "  $BASE_NAME$t"
	ip link set down dev "$BASE_NAME$t"
	ip tuntap del mode tap "$BASE_NAME$t"
done

echo ..done.
exit 0
