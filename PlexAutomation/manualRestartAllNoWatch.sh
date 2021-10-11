#!/bin/bash

sudo umount /media/PlexMediaFiles/Media;
sudo umount /media/PlexMediaFiles;
sudo umount /media/PlexMediaFiles_Backup;
sleep 10;
sudo mount /dev/sda1 /media/PlexMediaFiles;
sudo mount /dev/sdb1 /media/PlexMediaFiles_Backup;
sudo service plexmediaserver restart
