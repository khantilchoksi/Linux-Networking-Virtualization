#!/bin/bash

if [ "$#" -lt 2 ]; then
        echo "Two arguments are required. Granularity and Total Time"
        exit
fi

if [ ! -f ./cpu_load_avg.csv ]; then
        printf "timestamp, 1 min load average, 5 min load average, 15 min load average\n" >> cpu_load_avg.csv
fi

counter=0
while [ $counter -lt $2 ];
do
   top -b -n  1  | awk '/load average/ { printf "%s, %s %s %s\n", $3, $12, $13, $14 }' >> cpu_load_avg.csv
   counter=$[$counter + $1]
   sleep $1
done
