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
