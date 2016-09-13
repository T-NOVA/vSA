#!/bin/bash

BASE_NAME="tap"

# check if root
if [ `whoami` != "root" ]; then
	echo "Must be run as root!"
	exit 1
fi

ARGS=1

if [ $# -ne "$ARGS" ]; then
	echo -e "Usage: $0 <i>\n  i - index of last device to be created\n  Creates i+1 devices."
	exit $E_BADARGS
fi

echo "Creating $(($1+1)) tap devices.."

for t in $(seq 0 $1); do
	echo "  $BASE_NAME$t"
	ip tuntap add mode tap "$BASE_NAME$t"
done

echo ..done.
exit 0
