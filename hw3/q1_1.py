import sys
import libvirt
from xml.dom import minidom

def create_connection():
    conn = libvirt.open('qemu:///system')
    if not conn:
        print "Connection to quemu faile!"
        exit(1)
    return conn

def list_vm_objects(conn):
    domainIDs = conn.listDomainsID()
    if len(domainIDs) == 0:
        print "No active domains in current hypervisor"

    vm_id_list = [] + domainIDs
    print("Active Domain IDs: "+str(vm_id_list))

    # Fetching VM objects from IDs
    vm_objects_list = []
    for vm_id in vm_id_list:
	    vm_objects_list.append(conn.lookupByID(vm_id))

    return vm_objects_list

def list_macs(vm_list):
    for vm in vm_list:
        vm_xml = minidom.parseString(vm.XMLDesc(0))
        interface_types = vm_xml.getElementyByTagsName('interface')
        print('interface type: '+interface_types.getAttribute('type'))
        # interfaceNodes = interface_types.childNodes
        # for interfaceNode in interfaceNodes
        for interface in interface_types:
            mac_tag = interface.getElementyByTagsName('mac')
            mac_addresses = mac_tag.getAttribute('address')
            print('mac address: '+mac_addresses)


def list_ips():
    print('List IPS')


def resolve_ips():
    print('List IPS')

def resolve_macs():
    print('List IPS')

if __name__ == "__main__":
    connection = create_connection()
    vm_list = list_vm_objects(connection)
    list_macs(vm_list)