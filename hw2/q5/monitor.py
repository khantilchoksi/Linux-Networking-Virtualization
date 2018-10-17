import sys
import libvirt
import random
import os
import collections
import datetime
import argparse
from time import sleep

py_parser = argparse.ArgumentParser(description='Monitor script')

py_parser.add_argument('order', nargs=1, choices = ["CPU","MEM"], help="order to sort by")
py_parser.add_argument('--threshold', nargs=1, type = float, help="threshold CPU value")
py_parser.add_argument('--polling_interval', nargs=1, type = float, help="polling interval value")
py_parser.add_argument('--moving_window', nargs=1, type = int, help="moving window value")

py_args = py_parser.parse_args()

order = py_args.order[0]

if not py_args.threshold:
	threshold = 0
else:
	threshold = py_args.threshold[0]

conn = libvirt.open('qemu:///system')
if not conn:
	print "Connection failed"
	exit(1)

domainIDs = conn.listDomainsID()
if len(domainIDs) == 0:
	print "No active domains"

vm_id_list = [] + domainIDs
stats = []

for vm_id in vm_id_list:
	vm = conn.lookupByID(vm_id)
	cpu_stats = vm.getCPUStats(True)[0]
	mem_stats = vm.memoryStats()
	vcpus = vm.maxVcpus()
	stats.append([vm_id, cpu_stats['cpu_time']*1.0,\
	1 - mem_stats['available']*1.0/mem_stats['actual'], vcpus, vm])
	
sleep(1)

for indx, stat in enumerate(stats):
	vm = stat[-1]
	cpu_stats = vm.getCPUStats(True)[0]
	stats[indx][1] = (cpu_stats['cpu_time'] - stats[indx][1])/10**9
	stats[indx][1] = (stats[indx][1]*100)/stats[indx][3]
	if stats[indx][1] > 100:
		stats[indx][1] = 100

#Sort by CPU or MEM	
if order == "CPU":
	stats.sort(key=lambda x: x[1])
else:
	stats.sort(key=lambda x: x[2])

#Logging
if not os.path.isfile("alerts.csv"):
	log_file = open("alerts.csv",'w')
	log_file.write("VM name, timestamp, CPU usage\n")
else:
	log_file = open("alerts.csv",'a')

log_op = ""
print_op = ""
for vm_stat in stats:
	#Printing sorted list
	print "ID : ", vm_stat[0], " CPU usage : ", vm_stat[1]\
	, " MEM usage : ", vm_stat[2]
	#If cpu > threshold, log and print
	if vm_stat[1] > threshold:
		log_op += vm_stat[-1].name()+", "+str(datetime.datetime.now())+", "+str(vm_stat[1])+"\n"
		print_op += vm_stat[-1].name()+", "+str(datetime.datetime.now())+", "+str(vm_stat[1])+"\n"

log_file.write(log_op)
print "\n",print_op

#Bonus
if py_args.polling_interval==None or py_args.moving_window==None:
	exit(1)

poll_int = py_args.polling_interval[0]
mov_wind = py_args.moving_window[0]

prev_poll_time = {}
curr_poll_time = {}
polled_values = collections.defaultdict(list)

for indx, stat in enumerate(stats):
	vm = stat[-1]
	cpu_stats = vm.getCPUStats(True)[0]
	prev_poll_time[stat[0]] = cpu_stats['cpu_time']

if not os.path.isfile("mov_avgs.csv"):
	mavgs = open("mov_avgs.csv",'w')
	mavgs.write("VM ID, Moving average CPU usage\n")
else:
	mavgs = open("mov_avgs.csv",'a')

poll_timer = 0
try:
	while True:
		sleep(poll_int)
		 
		if poll_timer >= mov_wind*poll_int:
			#Log the moving window averages
			
			unsorted_list = []
			for v in polled_values:
				unsorted_list.append([v, sum(polled_values[v])/len(polled_values[v])])	
				polled_values[v].pop(0)
			unsorted_list.sort(key = lambda x: x[1])
			for v in unsorted_list:
				mavgs.write(str(v[0])+", "+str(v[1])+"\n")	
			#print unsorted_list
	
		for indx, stat in enumerate(stats):
	        	vm = stat[-1]
	        	cpu_stats = vm.getCPUStats(True)[0]
	        	curr_poll_time[stat[0]] = cpu_stats['cpu_time']
			polled_values[stat[0]].append(100*(curr_poll_time[stat[0]] - \
			prev_poll_time[stat[0]])/(10**9 * poll_int * stats[indx][3]))
			prev_poll_time[stat[0]] = curr_poll_time[stat[0]]
			#print polled_values
		poll_timer += poll_int
except:
	mavgs.close()
	exit(0)
