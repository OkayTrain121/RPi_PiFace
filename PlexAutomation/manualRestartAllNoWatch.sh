#!/bin/bash

sudo umount /mnt/plexmedia/Media; sudo umount /mnt/plexmedia; sleep 10; sudo mount /dev/sdb1 /mnt/plexmedia;
sudo service plexmediaserver restart

