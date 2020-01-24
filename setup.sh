#!/bin/bash

if [ ! -h /usr/bin/rmv-lcd.py ]; then
	sudo ln -s $(pwd)/rmv-lcd.py /usr/bin/rmv-lcd.py
fi
sudo cp ./config.json /etc/rmv-pi/
sudo cp ./rmv-lcd.service /etc/systemd/system/
sudo systemctl enable rmv-lcd.service
sudo systemctl restart rmv-lcd.service
