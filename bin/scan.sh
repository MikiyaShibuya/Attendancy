#!/bin/bash

SUBNET_HEAD=$1
START_SUBNET_IP=$2
END_SUBNET_IP=$3

SCRIPT_PATH=$(cd $(dirname $0); pwd)/../

for n in $(seq $START_SUBNET_IP $END_SUBNET_IP);do
	IP="$SUBNET_HEAD.$n"
	MAC=$(bash $SCRIPT_PATH/bin/ip2mac.sh $IP)
	if [ -n "$MAC" ];then
		echo $MAC
	fi
done

