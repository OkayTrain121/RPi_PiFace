syncLibraries.sh is invoked everytime at reboot. Just check if
there aren't multiple instances over time.

Other things to remember:
1. Alter the script files to indicate desired mount/umount points
2. This folder is placed in the Desktop (for crontab purposes)

Bloating issues of Plex stuff:
figure out space eating stuff in /var/lib/plexmediaserver using sudo du -h -d 1
and follow the apt instructions
1. https://support.plex.tv/articles/202529153-why-is-my-plex-media-server-directory-so-large/
2. https://forums.plex.tv/t/how-to-clean-up-the-huge-cache-folder/503871
3. Use a cronjob to clear out cache every 7 days as some cache files are not cleared by
the automated Scheduled Tasks on the server.

