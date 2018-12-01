import os
def get_next_subnet():
	try:
		f = open("ips.txt","r")
	except:
		f = open("ips.txt","w")
		f.write("100.0.1.0/24")
		f.close()
		f = open("ips.txt","r")
	curr_subnet = f.read()
	subnet, ip = curr_subnet[-3:], curr_subnet[:-3]
	
	oct1, oct2, oct3, oct4 = (int(octect) for octect in ip.split("."))
	
	oct3 += 1
	if oct3 == 200:
		oct3 = 0
		oct2 += 1
		if oct2 == 200:
			oct2 = 0
			oct1 += 1
	next_ip = str(oct1)+"."+str(oct2)+"."\
			+str(oct3)+"."+str(oct4)+subnet
	f.close()
	f = open("ips.txt","w")
	f.write(next_ip)
	f.close()
	return next_ip

def get_curr_ips():
	f = open("ips.txt")
	curr_subnet = f.read()

	subnet, ip = curr_subnet[-3:], curr_subnet[:-3]
	
	oct1, oct2, oct3, oct4 = (octect for octect in ip.split("."))
	
	left_part = oct1+"."+oct2+"."+oct3+"."
	return left_part+"1"+subnet, left_part+"2"+subnet, left_part+"3"+subnet
	
def parse_csv(file_name):
	f = open(file_name,"r")

	line = f.readline()
	op_list = []
	
	while line:
		dev1, dev2, contype = (v.strip() for v in line.split(","))
		if contype == "Bridge":
			new_subnet = get_next_subnet()
			ip_list = get_curr_ips()
			command = 'sudo ansible-playbook bridge_containers.yaml '+\
			'--extra-vars "container1_name='+dev1+' container2_name='\
			+dev2+' leafc1_ip='+ip_list[0]+\
			' c1_ip='+ip_list[1]+' c2_ip='+ip_list[2]+'"'
			#print command
			ret = os.system(command)
			print ret
		elif contype == "L3":
			subnet_1 = get_next_subnet()
			ip_list1 = get_curr_ips()
			subnet_2 = get_next_subnet()
			ip_list2 = get_curr_ips()

			command = 'sudo ansible-playbook l3_containers.yaml '+\
			'--extra-vars "container1_name='+dev1+' container2_name='\
			+dev2+' leafc1_ip='+ip_list1[0]+' leafc2_ip='+ip_list2[0]+\
			' c1_ip='+ip_list1[1]+' c2_ip='+ip_list2[1]+' c1_netw='+subnet_1+\
			' c2_netw='+subnet_2+'"'
			#print command
			ret = os.system(command)
			print ret

		op_list.append((dev1.strip(),dev2.strip(), contype.strip()))
		line = f.readline()



