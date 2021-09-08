# pve-snippets

Add hook snippet to VM:
```
qm set <vmid> --hookscript sync:snippets/change_mac.pl
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
