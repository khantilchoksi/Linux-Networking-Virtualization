#!/bin/bash

ip link add $3 type veth peer name $4
CONTAINER_ID=$(docker inspect --format '{{.State.Pid}}' $2)
sudo ip link set netns $CONTAINER_ID dev $4
sudo brctl addif $1 $3
sudo ip link set $1 up
sudo ip link set $3 up
sudo nsenter -t $CONTAINER_ID -n ip link set $4 up
sudo nsenter -t $CONTAINER_ID -n ip addr add $5 dev $4

