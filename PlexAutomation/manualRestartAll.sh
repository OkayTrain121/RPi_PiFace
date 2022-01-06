#!/bin/bash

sudo umount /media/pi/PlexMediaFiles;
sudo umount /media/pi/PlexMediaFiles_Backup;
sleep 10;
sudo mount /dev/sda1 /media/pi/PlexMediaFiles;
sudo mount /dev/sdb1 /media/pi/PlexMediaFiles_Backup;
sudo service plexmediaserver restart;

export LD_LIBRARY_PATH="/usr/lib/plexmediaserver/lib";
sudo su -s /bin/bash plex -c "/usr/lib/plexmediaserver/Plex\ Media\ Scanner --scan --refresh --force"
#su plex /home/pi/Desktop/PlexAutomation/scan.sh
#sudo killall -9 syncLibraries.sh; /home/pi/Desktop/PlexAutomation/syncLibraries.sh;
