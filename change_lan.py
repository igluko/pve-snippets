#!/usr/bin/python3

import sys, os, json

vmid = sys.argv[1]
phase = sys.argv[2]
hostname = os.uname()[1]
conf_file = sys.path[0]+'/'+'change_lan.conf'

def get_conf(file):
    if os.path.isfile(file):
        with open(file,'r') as conf_file:
            try:
                data = json.load(conf_file)
            except json.decoder.JSONDecodeError:
                print('Not valid json in file ' + file)
                sys.exit()
        conf_file.close()
        return(data['conf'])
    else:
        print('Conf file ' + file + ' not found')
        sys.exit()

def find_conf(configs, vmid, hostname):
    result = []
    for config in configs:
        if (config['Hostname'] == hostname) and (str(config['VMID']) == vmid):
            result = config
    if len(result) == 0:
       print('Not found config for ' + hostname + ':' + vmid)
       sys.exit()
    return(result)
            
def check_mac(new_conf, vmid, hostname):
    
    cmd = 'pvesh get /nodes/' + hostname + '/qemu/' + vmid + '/config -output-format json'
    conf_vm = json.load(os.popen(cmd))
    net_conf_vm = ''
    for k, v in conf_vm.items():
        if 'net' in k:
            net_conf_vm += v   
    if (new_conf['MAC_UP'] in net_conf_vm) and (new_conf['MAC_DOWN'] in net_conf_vm):
        pass
    else:
        sys.exit('Does not match MAC address')

def get_bash_conf(new_conf):
    res_conf = []
    res_conf.append('sed -i -r "s/(net.: virtio=)(' + new_conf['MAC_UP'] + ')(.*)(,link_down=1)/\\1\\2\\3/" /etc/pve/local/qemu-server/' + str(new_conf['VMID']) + '.conf')
    res_conf.append('sed -i -r "/,link_down=1/! s/(net.: virtio=)(' + new_conf['MAC_DOWN'] + ')(.*)/\\1\\2\\3,link_down=1/" /etc/pve/local/qemu-server/' + str(new_conf['VMID']) + '.conf')
    return(res_conf)

if phase == 'pre-start':
    try:
        print('Snippet started: pre-start')
        configs = get_conf(conf_file)
        new_conf = find_conf(configs, vmid, hostname)
        check_mac(new_conf, vmid, hostname)
        cmd_list = get_bash_conf(new_conf)
        for cmd in cmd_list:
            print('Command to execute: ' + cmd)
            status = os.system(cmd)
            if status != 0:
                sys.exit('The command completed with an error: ' + status)
        print('Snippet work done')
    except BaseException:
        print('Break snippet.')
        sys.exit()
