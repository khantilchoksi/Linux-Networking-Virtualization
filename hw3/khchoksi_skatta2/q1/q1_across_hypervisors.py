import sys
from time import sleep
import collections
import libvirt
import lxml.etree as le
from xml.dom import minidom
import paramiko

def create_connection(hypervisor_ip):
	conn = libvirt.open('qemu+tls://'+hypervisor_ip+'/system')
	if not conn:
		print ("Connection to quemu failed!")
		exit(1)
	return conn

def list_vm_objects(conn):
	domainIDs = conn.listDomainsID()
	if len(domainIDs) == 0:
		print ("No active domains in current hypervisor")
	
	vm_id_list = [] + domainIDs
	
	vm_objects_list = []
	for vm_id in vm_id_list:
		vm_objects_list.append(conn.lookupByID(vm_id))
	return vm_objects_list

def list_macs(vm_list):
	vm_mac_map = {}
	for vm in vm_list:
		vm_xml = minidom.parseString(vm.XMLDesc(0))
		interface_types = vm_xml.getElementsByTagName('interface')
		name_tag = vm_xml.getElementsByTagName('name')
		vm_name = name_tag[0].firstChild.nodeValue
		con_vm_map[vm] = vm_name
		for interface in interface_types:
			mac_tag = interface.getElementsByTagName('mac')
			mac_addresses = mac_tag[0].getAttribute('address')
			vm_mac_map[vm_name].append(mac_addresses)
	return vm_mac_map


def list_ips(vm_list):
	vm_ip_map = {}
	for dom in vm_list:
		ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
		for (name, val) in ifaces.iteritems():
			if val['addrs']:
				for ipaddr in val['addrs']:
					if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
						if ipaddr['addr'] != "127.0.0.1":
							vm_ip_map[con_vm_map[dom]].append(ipaddr['addr'])
	return vm_ip_map


# def del_mac_tags_reset(conn, name, macs):
# 	to_write = ""
# 	path = "/etc/libvirt/qemu/"+name+".xml"
# 	with open(path,'r') as f:
# 	    doc=le.parse(f)
# 	    for elem in doc.xpath('//*[attribute::address]'):
# 	        if elem.attrib['address'] in macs:
# 	            elem.attrib.pop('address')
# 	            parent=elem.getparent()
# 	            parent.remove(elem)
# 	    to_write = le.tostring(doc)
# 	f = open(path,"w")
# 	f.write(to_write)
# 	f.close()
# 	dom = conn.createXML(to_write, 0)
# 	if dom == None:
# 		print 'Unable to define persistent guest configuration.'
# 		exit(1)

def del_mac_tags_reset(hypervisor_ip, vm_name, vm_macs):

	# SSH to hypervisor
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hypervisor_ip, username='ece792', password='EcE792net!',log="./mylogs.log")

	# Copy python script
	sftp = ssh_client.open_sftp()
	sftp.put('./resolve_conflict.py', '~/resolve_conflict.py')
	sftp.close()

	# Run script with vmname and mac
	for vm_mac_address in vm_macs:
		stdoutput = ssh_client.exec_command('python ~/resolve_conflict.py '+vm_name+vm_mac_address)[1]
		for l in stdoutput:
			print l

	client.close()
	
	#if dom.create(dom) < 0:
	#	print "Can not boot guest domain"
	#	exit(1)	

con_vm_map = {}
VM_MAC_MAP = collections.defaultdict(list)
VM_IP_MAP = collections.defaultdict(list) 

if __name__ == "__main__":
	hypervisor_list = []
	hypervisor_list.append('192.168.124.15')
	hypervisor_vm_map = {}
	hypervisor_vm_ip_map = {}
	hypervisor_vm_mac_map = {}

	for hypervisor_ip in hypervisor_list:
		conn = create_connection(hypervisor_ip)
		vm_list = list_vm_objects(conn)
		hypervisor_vm_map[hypervisor_ip] = vm_list
		hypervisor_vm_mac_map[hypervisor_ip] = list_macs(vm_list)
		hypervisor_vm_ip_map[hypervisor_ip] = list_ips(vm_list)
	
	print "PART 1 : All MACs and IPs across all hypervisors"
	for hypervisor in hypervisor_vm_map:
		for name in hypervisor_vm_mac_map[hypervisor]:
			print "Domain name "+ name
			if name in hypervisor_vm_ip_map[hypervisor]:
				for ip_addr in hypervisor_vm_ip_map[hypervisor][name]:
					print "IP:\t" + ip_addr
			for mac_addr in hypervisor_vm_mac_map[hypervisor][name]:
				print "MAC:\t" + mac_addr
			print "\n"	
	

	unique_macs = set()
	unique_ips = set()

	conf_vms = []
	conf1_vms = []

	to_resolve = []
	to_resolve_ip = []

	for hypervisor in hypervisor_vm_mac_map:
		for vm_name in hypervisor_vm_mac_map[hypervisor]:
			for mac_addr in hypervisor_vm_mac_map[hypervisor][vm_name]:
				if mac_addr in unique_macs:
					conf_vms.append((vm_name, mac_addr))
					to_resolve.append((hypervisor_ip,vm_name, mac_addr))
				unique_macs.add(mac_addr)

		for vm_name in hypervisor_vm_ip_map[hypervisor]:
			for ip_addr in hypervisor_vm_ip_map[hypervisor][vm_name]:
				if ip_addr in unique_ips:
					conf1_vms.append((vm_name, ip_addr))
					to_resolve_ip.append((hypervisor_ip,vm_name, ip_addr))
				unique_ips.add(ip_addr)

	print "PART 2 : List of conflicting MAC addresses across all hypervisors"
	for tupl in to_resolve:
		print "Conflicting mac found for hypervisor " + tupl[0] + " with vm name "+ tupl[1]+"with mac " + tupl[2]



	VM_MAC_MAP = collections.defaultdict(list)
	for tupl in conf_vms:
		VM_MAC_MAP[tupl[0]].append(tupl[1])
	if len(to_resolve) == 0:
		print "PART 3 : No conflicts to resolve"
		sys.exit(0)
	else:
		print "PART 3 : Resolved MACS Conflicts"
		unique_macs = set()
		unique_ips = set()

		conf_vms = []
		conf1_vms = []

		to_resolve = []
		to_resolve_ip = []

		for hypervisor in hypervisor_vm_mac_map:
			for vm_name in hypervisor_vm_mac_map[hypervisor]:
				for mac_addr in hypervisor_vm_mac_map[hypervisor][vm_name]:
					if mac_addr in unique_macs:
						to_resolve.append((hypervisor_ip,vm_name, mac_addr))
						# Resolving here
						del_mac_tags_reset(hypervisor_ip,vm_name, mac_addr)
					unique_macs.add(mac_addr)
	sleep(10)
	print "PART 4 - After resolving conflicts"

		for hypervisor_ip in hypervisor_list:
		conn = create_connection(hypervisor_ip)
		vm_list = list_vm_objects(conn)
		hypervisor_vm_map[hypervisor_ip] = vm_list
		hypervisor_vm_mac_map[hypervisor_ip] = list_macs(vm_list)
		hypervisor_vm_ip_map[hypervisor_ip] = list_ips(vm_list)
	
	print "PART 4 : All MACs and IPs across all hypervisors"
	for hypervisor in hypervisor_vm_map:
		for name in hypervisor_vm_mac_map[hypervisor]:
			print "Domain name "+ name
			if name in hypervisor_vm_ip_map[hypervisor]:
				for ip_addr in hypervisor_vm_ip_map[hypervisor][name]:
					print "IP:\t" + ip_addr
			for mac_addr in hypervisor_vm_mac_map[hypervisor][name]:
				print "MAC:\t" + mac_addr
			print "\n"

	
