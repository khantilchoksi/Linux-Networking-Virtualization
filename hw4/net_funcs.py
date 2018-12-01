
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
	return left_part+"1"+subnet, left_part+"2"+subnet
	
def parse_csv(file_name):
	f = open(file_name,"r")
	
	line = f.readline()
	print line	
	op_list = []
	
	while line:
		print line
		dev1, dev2, contype = line.split()
		print dev1, dev2, contype
		#op_list.append((dev1.strip(),dev2.strip(), contype.strip()))
		line = f.readline()
	return iter(op_list)
