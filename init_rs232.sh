#!/bin/sh

echo 'configuring rs232 uhart...'
sudo echo 'dtoverlay=sc16is752-spi1,int_pin=24' >> /boot/config.txt
echo 'installing rs232 uhart dependencies...'
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install RPi.GPIO
sudo apt-get install python3-serial
echo 'rs232 uhart initialized, rebooting'
sudo reboot
