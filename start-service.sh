#!/bin/sh

sudo systemctl stop hificontrol.service
sudo systemctl start hificontrol.service
sudo systemctl status hificontrol.service

