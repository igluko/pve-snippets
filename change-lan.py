#!/usr/bin/python3

import sys, os, json

vmid = sys.argv[1]
phase = sys.argv[2]
hostname = os.uname()[1]

if hostname.startswith("prod-prefix"):
    print('State: ' + phase + ". Prod - exit.")
    sys.exit()

prod_host = {
    'name':'master-hostname',
    'net0':'virtio=AA:AA:AA:AA:AA:AA,bridge=vmbr0,firewall=1',
    'net1':'virtio=BB:BB:BB:BB:BB:BB,bridge=vmbr0,firewall=1,link_down=1'
    }

reserve_host = {
    'name':'slave-hostname',
    'net0':'virtio=AA:AA:AA:AA:AA:AA,bridge=vmbr0,firewall=1,link_down=1',
    'net1':'virtio=BB:BB:BB:BB:BB:BB,bridge=vmbr0,firewall=1'
    }

def check_conf(prod_host, reserve_host, hostname):
    
    if hostname == prod_host['name']:
        print('Start on prod server: ' + prod_host['name'] )
        return('prod')
    elif hostname == reserve_host['name']:
        print('Start on reserve server: ' + reserve_host['name'])
        return('reserve')
    else:
         sys.exit('Start on unknown host: hostname')
    
def set_new_conf(from_host, to_host):
    
    cmd = 'pvesh get /nodes/' + hostname + '/qemu/' + vmid + '/config -output-format json'
    conf = json.load(os.popen(cmd)) 
    
    res_conf = []
    
    for k, v in to_host.items():
        if 'net' in k:
            if conf[k] == v:
                print(k + ' conf is OK')
            elif conf[k] == from_host[k]:
                print('Configuration ' + k + ' needs to be changed.')
                res_conf.append("sed -i 's/" + from_host[k] + '/' + to_host[k] + "/'  /etc/pve/qemu-server/" + vmid + '.conf')
            else:
                sys.exit('Unknown configuration for ' + k + ' on host')
    return(res_conf)


if phase == 'pre-start':

   print('Snippet started: pre-start')

   host_status = check_conf(prod_host, reserve_host, hostname)

   if host_status == 'prod':
       cmd_list = set_new_conf(reserve_host, prod_host)
   elif host_status == 'reserve':
       cmd_list = set_new_conf(prod_host, reserve_host)

   for cmd in cmd_list:
       print('Command to execute: ' + cmd)
       status = os.system(cmd)
       if status != 0:
           sys.exit('The command completed with an error: ' + status)
   print('Snippet work done')
