#!/bin/bash

sudo umount /media/pi/PlexMediaFiles;
sudo umount /media/pi/PlexMediaFiles_Backup;
sleep 10;
sudo mount /dev/sda1 /media/pi/PlexMediaFiles;
sudo mount /dev/sdb1 /media/pi/PlexMediaFiles_Backup;
sudo service plexmediaserver restart
