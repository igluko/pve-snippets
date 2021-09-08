#!/usr/bin/perl

# Exmple hook script for PVE guests (hookscript config option)
# You can set this via pct/qm with
# pct set <vmid> -hookscript <volume-id>
# qm set <vmid> -hookscript <volume-id>
# where <volume-id> has to be an executable file in the snippets folder
# of any storage with directories e.g.:
# qm set 100 -hookscript local:snippets/hookscript.pl

use strict;
use warnings;

print "GUEST HOOK: " . join(' ', @ARGV). "\n";

# First argument is the vmid

my $vmid = shift;

# Second argument is the phase

my $phase = shift;

if ($phase eq 'pre-start') {

    # First phase 'pre-start' will be executed before the guest
    # ist started. Exiting with a code != 0 will abort the start

    print "$vmid is starting, doing preparations.\n";
    my $mac_up = `cat /root/Sync/mac/$vmid | grep \$(hostname) | cut -d "," -f 2 | tr -d '\n'`;
    my $mac_down = `cat /root/Sync/mac/$vmid | grep -v \$(hostname) | cut -d "," -f 2 | tr -d '\n'`;
    print "$mac_up\n";
    print "$mac_down\n";

    # change config with API not working - config lock
    # mac up
    #sed -i -r "s/(net.: virtio=)(..:..:..:..:..:..)(.*)(,link_down=1)/\1\2\3/" 950.conf
    `sed -i -r "s/(net.: virtio=)($mac_up)(.*)(,link_down=1)/\\1\\2\\3/" /etc/pve/local/qemu-server/$vmid.conf`;
    
    # mac down
    #sed -i -r "/,link_down=1/! s/(net.: virtio=)(..:..:..:..:..:..)(.*)/\1\2\3,link_down=1/" 950.conf    
    `sed -i -r "/,link_down=1/! s/(net.: virtio=)($mac_down)(.*)/\\1\\2\\3,link_down=1/" /etc/pve/local/qemu-server/$vmid.conf`;        
    
    # print "preparations failed, aborting."
    # exit(1);

} elsif ($phase eq 'post-start') {

    # Second phase 'post-start' will be executed after the guest
    # successfully started.

    print "$vmid started successfully.\n";

} elsif ($phase eq 'pre-stop') {

    # Third phase 'pre-stop' will be executed before stopping the guest
    # via the API. Will not be executed if the guest is stopped from
    # within e.g., with a 'poweroff'

    print "$vmid will be stopped.\n";

} elsif ($phase eq 'post-stop') {

    # Last phase 'post-stop' will be executed after the guest stopped.
    # This should even be executed in case the guest crashes or stopped
    # unexpectedly.

    print "$vmid stopped. Doing cleanup.\n";

} else {
    die "got unknown phase '$phase'\n";
}

exit(0);
