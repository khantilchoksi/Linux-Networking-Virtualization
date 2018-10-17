import sys
import libvirt

conn = libvirt.open('qemu:///system')

if conn == None:
	print('Connection failed')
	exit(1)

node_info = conn.getInfo()

print "Hostname : ", conn.getHostname()
print "Number of vcpus : ", conn.getMaxVcpus(None)
print "Memory size : ", node_info[1]
print "Clock speed of CPUs : ", node_info[3]
print "Number of CPUs : ", node_info[2]
print "Virtualization type: ", conn.getType()
print "Canonical URI : ", conn.getURI()

conn.close()
exit(1)






