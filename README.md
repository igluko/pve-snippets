# pve-snippets

## change_mac
This hook script change MAC before VM started. This is necessary during the failover.

File required: /root/Sync/mac/<vmid>
```
AX101-Helsinki-03,DA:E6:D3:96:5D:7F
AX61-Falkenstein-03,AA:3C:F3:31:47:02
```
## net_up_down
This hook script change net state before VM started. This is necessary during the failover.
The script raises the mac address which is associated with the local host and down the other.
  
File required: /root/Sync/mac/<vmid>
```
AX101-Helsinki-03,DA:E6:D3:96:5D:7F
AX61-Falkenstein-03,AA:3C:F3:31:47:02
```
