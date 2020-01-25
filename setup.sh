#!/bin/bash

if [ ! -h /usr/bin/rmv-lcd.py ]; then
	sudo ln -s $(pwd)/rmv-lcd.py /usr/bin/rmv-lcd.py
fi
if [ ! -d /etc/rmv-lcd ]; then
	sudo mkdir -p /etc/rmv-lcd
fi
if [ ! -h /etc/rmv-lcd/config.json ]; then
	sudo ln -s $(pwd)/config.json /etc/rmv-pi/config.json
fi
sudo cp ./rmv-lcd.service /etc/systemd/system/
sudo systemctl enable rmv-lcd.service
sudo systemctl restart rmv-lcd.service
