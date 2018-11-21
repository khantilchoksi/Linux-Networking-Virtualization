Provide the Guests (VM) requirements that you want to create inside guests_vars.yml and bridges requirements inside networks_vars.yml.

run script with sudo command:
$ sudo ansible-playbook q2.yml 

Assumptions:
- Client has to set interface ip (which is connected with OVS bridge in routed mode)