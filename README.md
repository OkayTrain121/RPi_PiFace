# RPi_PiFace
PiFace CAD

Contains the python script to handle key interrupts and corresponding display requirements.

Some additional changes have been implemented in the pifacecad lib to properly handle key interrupts
and some known bug fixes have been patched.

Functionality has been implemented to automatically run cad_master.py on startup.
It is achieved using systemctl and running the python program as a system process.
Unit file for system.d is uploaded.

In order to make mypiface.service enabled automatically on boot:
1. Place the mypiface.service in /lib/systemd/system/
2. Create symbolic link with all permissions in /etc/systemd/system/multi-user.target.wants
3. Enable the service and start it using:  
  sudo systemctl status mypiface.service  
  sudo systemctl enable mypiface.service  
  sudo systemctl start mypiface.service
4. Ofcourse, pifacecad must be installed as explained in https://github.com/piface/pifacecad
5. The files that need to be altered post installation in Step 4 are placed in their respective  
  folders in this repo.
  
# Other items
This repo also contains other items, such as PlexMediaAutomation
In order to install Plex:
1. Follow https://pimylifeup.com/raspberry-pi-plex-server/
2. Update transcoder directory in the GUI to a folder in the hdd.
3. Use crontab scripts to automate timed restarts. Just copy crontab from repo.
4. Create symlink for media files in /home/pi/
