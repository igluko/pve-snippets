# pve-snippets
Add storage "sync" for store snippets:
```
pvesm add dir sync --path /root/Sync --content snippets
```

Copy snippet template to storage
```
cp /usr/share/pve-docs/examples/guest-example-hookscript.pl /root/Sync/snippets/
```
Add example snippet to VM:
```
qm set <vmid> --hookscript sync:snippets/guest-example-hookscript.pl
```
## change_mac
This hook script change MAC before VM started. This is necessary during the failover.

File required: /root/Sync/mac/<vmid>
```
hostname_node_1,FF:FF:FF:FF:FF:FF
hostname_node_2,AA:AA:AA:AA:AA:AA
```
## net_up_down
This hook script change net state before VM started. This is necessary during the failover.
The script raises the mac address which is associated with the local host and down the other.
  
File required: /root/Sync/mac/<vmid>
```
hostname_node_1,FF:FF:FF:FF:FF:FF
hostname_node_2,AA:AA:AA:AA:AA:AA
```
## change_lan.py
This hook script change net state before VM started. This is necessary during the failover.
The script raises the mac address which is associated with the local host and down the other.
  
File required: /root/Sync/mac/change_lan.conf
```
{
    "conf":
    [
        {"Hostname":"pve", "VMID": 100, "MAC_UP": "AA:AA:AA:AA:AA:AA", "MAC_DOWN": "BB:BB:BB:BB:BB:BB"},
        {"Hostname":"pve02", "VMID": 100, "MAC_UP": "BB:BB:BB:BB:BB:BB", "MAC_DOWN": "AA:AA:AA:AA:AA:AA"}
    ]
}
```
