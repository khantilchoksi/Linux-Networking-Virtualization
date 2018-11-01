import sys
from time import sleep
import collections
import libvirt
import lxml.etree as le
from xml.dom import minidom

def create_connection():
	conn = libvirt.open('qemu:///system')
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
	for vm in vm_list:
		vm_xml = minidom.parseString(vm.XMLDesc(0))
		interface_types = vm_xml.getElementsByTagName('interface')
		name_tag = vm_xml.getElementsByTagName('name')
		vm_name = name_tag[0].firstChild.nodeValue
		con_vm_map[vm] = vm_name
		for interface in interface_types:
			mac_tag = interface.getElementsByTagName('mac')
			mac_addresses = mac_tag[0].getAttribute('address')
			VM_MAC_MAP[vm_name].append(mac_addresses)


def list_ips(conn):
	for dom in conn:
		ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
		for (name, val) in ifaces.iteritems():
			if val['addrs']:
				for ipaddr in val['addrs']:
					if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
						if ipaddr['addr'] != "127.0.0.1":
							VM_IP_MAP[con_vm_map[dom]].append(ipaddr['addr'])


def del_mac_tags_reset(conn, name, macs):
	to_write = ""
	path = "/etc/libvirt/qemu/"+name+".xml"
	with open(path,'r') as f:
	    doc=le.parse(f)
	    for elem in doc.xpath('//*[attribute::address]'):
	        if elem.attrib['address'] in macs:
	            elem.attrib.pop('address')
	            parent=elem.getparent()
	            parent.remove(elem)
	    to_write = le.tostring(doc)
	f = open(path,"w")
	f.write(to_write)
	f.close()
	dom = conn.createXML(to_write, 0)
	if dom == None:
		print 'Unable to define persistent guest configuration.'
		exit(1)
	
	#if dom.create(dom) < 0:
	#	print "Can not boot guest domain"
	#	exit(1)	

con_vm_map = {}
VM_MAC_MAP = collections.defaultdict(list)
VM_IP_MAP = collections.defaultdict(list) 

if __name__ == "__main__":
	
	conn = create_connection()
	vm_list = list_vm_objects(conn)
	list_macs(vm_list)
	list_ips(vm_list)
	
	print "PART 1 : All MACs and IPs"
	for name in VM_MAC_MAP:
		print "Domain name "+ name
		if name in VM_IP_MAP:
			for ip_addr in VM_IP_MAP[name]:
				print "IP:\t" + ip_addr
		for mac_addr in VM_MAC_MAP[name]:
			print "MAC:\t" + mac_addr
		print "\n"	
	

	unique_macs = set()
	unique_ips = set()

	conf_vms = []
	conf1_vms = []

	for vm_name in VM_MAC_MAP:
		for mac_addr in VM_MAC_MAP[vm_name]:
			if mac_addr in unique_macs:
				conf_vms.append((vm_name, mac_addr))
			unique_macs.add(mac_addr)

	for vm_name in VM_IP_MAP:
		for ip_addr in VM_IP_MAP[vm_name]:
			if ip_addr in unique_ips:
				conf1_vms.append((vm_name, ip_addr))
			unique_ips.add(ip_addr)
	print "PART 2 : List of conflicting MAC addresses"
	for tupl in conf_vms:
		print "Conflicting mac found for " + tupl[0] + " with mac " + tupl[1]

	VM_MAC_MAP = collections.defaultdict(list)
	for tupl in conf_vms:
		VM_MAC_MAP[tupl[0]].append(tupl[1])
	if len(conf_vms) == 0:
		print "PART 3 : No conflicts to resolve"
		sys.exit(0)
	else:
		print "PART 3 : Resolving MAC conflicts"
		for vm_name in VM_MAC_MAP:
			dom = conn.lookupByName(vm_name)
			dom.shutdown()
			dom.destroy()
			del_mac_tags_reset(conn, vm_name, VM_MAC_MAP[vm_name])
	sleep(10)
	print "PART 4 - After resolving conflicts"
	conn = create_connection()
	vm_list = list_vm_objects(conn)
	list_macs(vm_list)
	list_ips(vm_list)

	for name in VM_MAC_MAP:
		print "Domain name "+ name
		if name in VM_IP_MAP:
			for ip_addr in VM_IP_MAP[name]:
				print "IP:\t" + ip_addr
		for mac_addr in VM_MAC_MAP[name]:
			print "MAC:\t" + mac_addr
		print "\n"	
	
