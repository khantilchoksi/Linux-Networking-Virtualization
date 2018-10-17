import sys
import libvirt
import random

conn = libvirt.open('qemu:///system')
if not conn:
	print "Connection failed"
	exit(1)

domainIDs = conn.listDomainsID()
if len(domainIDs) == 0:
	print "No active domains"
randomid = random.sample(domainIDs, 1)

rdom = conn.lookupByID(randomid[0])

state, maxmem, mem, cpus, cput = rdom.info()
print "UUID of the guest vm : ", rdom.UUIDString()
print "OS type of the guest vm : ", rdom.OSType()
print "Max vcpus of the guest vm : ", str(rdom.maxVcpus())
print "State of the guest vm : ", str(state)
print "Name of the guest vm : ", rdom.name()
print "Max memory of the guest vm : ", str(maxmem)
print "Number of cpus in the guest vm : ", str(cpus)

conn.close()
exit(1)





