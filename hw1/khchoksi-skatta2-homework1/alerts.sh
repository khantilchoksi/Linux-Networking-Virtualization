#!/bin/bash

if [ "$#" -lt 2 ]; then
        echo "Two arguments are required. Granularity and Total Time"
        exit
fi

if [ ! -f ./alert.csv ]; then
        printf "timestamp, alert string, CPU load average \n" >> alert.csv
fi

counter=0

while [ $counter -lt $2 ];
do

        extract_load=`top -b -n  1  | awk '/load average/ { printf "%s, %.2f %.2f %.2f\n", $3, $12, $13, $14 }'`
        echo $extract_load
        IFS=', ' read -r -a load_avg <<< "$extract_load"
        echo "Timestamp: ${load_avg[0]}"
        echo "1 min load average : ${load_avg[1]}"

        is_high=`printf ${load_avg[1]}'\n'$3'\n' | sort -g | head -1`

        echo "${load_avg[0]}, ${load_avg[1]}" >> graph.csv
        if [ $is_high == $3 ]; then
                echo "${load_avg[0]}, HIGH CPU usage, ${load_avg[1]}" >> alert.csv
        fi

        if [[ ${load_avg[2]} > $4 && ${load_avg[1]} > ${load_avg[2]}  &&  ${load_avg[2]} > ${load_avg[3]} ]]; then
                echo "VERY HIGH"
                echo "${load_avg[0]}, Very HIGH CPU usage, ${load_avg[1]}" >> alert.csv
        fi

        counter=$[$counter+$1]
        sleep $1
done
