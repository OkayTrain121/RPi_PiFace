# RPi_PiFace
PiFace CAD

Contains the python script to handle key interrupts and corresponding display requirements.

Some additional changes have been implemented in the pifacecad lib to properly handle key interrupts
and some known bug fixes have been patched.

Functionality has been implemented to automatically run cad_master.py on startup.
It is achieved using systemctl and running the python program as a system process.
Unit file for system.d is uploaded.
