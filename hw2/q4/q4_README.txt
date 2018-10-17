- (Also explained this in report) 
- Make sure to install Ansible on your host machine / VM.  
- If not,
Prerequisite: Install ansible on host machine
$ sudo apt-add-repository ppa:ansible/ansible
$ sudo apt-get update
$ sudo apt-get install ansible
$ ansible --version
	ansible 2.7.0


- Please make sure to run the ansible script with X11 forwarding.
- The script will wait for configuration of VM using GUI (which can't be automated)  

$ sudo ansible-playbook q4_1.yml --extra-vars="/home/ece792/iso/CentOS-7-x86_64-Minimal-1804.iso"

Intermediate steps to setup ssh:
Create a new NAT bridge virbr1 so that both the newly created vms can have ips.
Create new network: khchoksiNETWORK3.xml
<network>
  <name>khchoksiNETWORK3</name>
  <uuid>eadcd6b7-c89a-43b5-9fe0-407eb0034038</uuid>
  <forward mode='nat'/>
  <bridge name='virbr1' stp='on' delay='0'/>
  <mac address='52:54:00:9f:f8:b6'/>
  <ip address='192.168.119.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.119.2' end='192.168.119.254'/>
    </dhcp>
  </ip>
</network>

$ brctl addbr virbr1
$ virsh net- start khchoksiNETWORK3
Add this interface to both the VMs and restart them. 
   
<interface type='network'>
      <source network='khchoksiNETWORK3'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x0a' function='0x0'/>
</interface>

Get the ips of both the vms (if not assigned, do dhcpclient).
Create SSH key pairs on host machine 
$ ssh-keygen 
and then follow the command
Copy public keys to both guest machines
$ ssh-copy-id -i ./keys/vm_rsa.pub root@192.168.119.58
$ ssh-copy-id -i ./keys/vm_rsa.pub root@192.168.119.252
VII.	Create new inventory file as follows: 
	[vms]
localhost ansible_connection=local
192.168.119.58 ansible_ssh_user=root ansible_ssh_private_key_file=./keys/vm_rsa
192.168.119.252 ansible_ssh_user=root ansible_ssh_private_key_file=./keys/vm_rsa

Q4_2


$ sudo ansible-playbook q4_2.yml -i ./inventory --extra-vars "time=7"

Logs will be generated at: /var/customlogs/logs.csv  (Attached within zip:-> q4_2_logs.csv)
Note: Ansible playbook will create ‘customlogs’ directory if not present.
