#!/bin/bash

sudo umount /mnt/plexmedia/Media;
sudo umount /mnt/plexmedia;
sleep 10;
sudo mount /dev/sdb1 /mnt/plexmedia;
sudo service plexmediaserver restart;

export LD_LIBRARY_PATH="/usr/lib/plexmediaserver/lib";
sudo su -s /bin/bash plex -c "/usr/lib/plexmediaserver/Plex\ Media\ Scanner --scan --refresh --force";
#su plex /home/pi/Desktop/PlexAutomation/scan.sh
#sudo killall -9 syncLibraries.sh; /home/pi/Desktop/PlexAutomation/syncLibraries.sh;
