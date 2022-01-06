#!/bin/bash

# This is probably not working as the path to the media has been changed
inotifywait -r -m /mnt/plexmedia/ -e create -e moved_to | 
	while read path file action; 
	do
		echo "New file found in the library! at $(date)" >> /home/pi/Desktop/PlexAutomation/log.txt
		sleep 5m
		export LD_LIBRARY_PATH="/usr/lib/plexmediaserver"
		sudo su -s /bin/bash plex -c "/usr/lib/plexmediaserver/Plex\ Media\ Scanner --scan --refresh --force"
	done
