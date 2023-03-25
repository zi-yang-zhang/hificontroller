#!/bin/sh

sudo systemctl stop hificontrol.service
sudo systemctl start hificontrol.service
sudo systemctl status hificontrol.service
sudo journalctl -f -n 1000 -u hificontrol.service
