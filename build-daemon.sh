#!/bin/sh
echo 'buidling hificontrol service...'
sudo cp /home/pi/hificontroller/hificontrol.service /lib/systemd/system/hificontrol.service
sudo chmod 644 /lib/systemd/system/hificontrol.service
chmod +x /home/pi/hificontroller/main.py
sudo systemctl daemon-reload
sudo systemctl enable hificontrol.service
echo 'hificontrol service built'


