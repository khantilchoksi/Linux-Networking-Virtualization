- Make sure to install Ansible on your host machine / VM.  
- If not, install Ansible: `sudo apt-get install ansible` and check by `ansible --version`
- Please make sure to run the ansible script with X11 forwarding.
- The script will wait for configuration of VM using GUI (which can't be automated)  
- TO DO: Take argument iso file

- ssh-keygen (on host machine)
- ssh-copy-id -i ./keys/vm_rsa.pub root@192.168.119.58
- ssh-copy-id -i ./keys/vm_rsa.pub root@192.168.119.252