#!/bin/sh

IP=$1

if [ -z "$IP" ];then
	echo "Usage:"
	echo "$0 [ip address]"
	exit 1
fi

MAC_ADDRESS_REGEX="\([0-9a-f]\{2\}:\)\{5\}[0-9a-f]\{2\}"
TIMEOUT=0.4s

TTL_LINE=$(timeout $TIMEOUT ping -c 1 $IP | grep ttl)

if [ -z "$TTL_LINE" ];then
	exit 0
else
	MAC_ADDRESS=$(arp $IP | grep -o "$MAC_ADDRESS_REGEX" | head -n 1)
	echo "$MAC_ADDRESS"
fi

