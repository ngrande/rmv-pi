#!/bin/bash

if [ ! -h /usr/bin/rmv-lcd.py ]; then
	sudo ln -s $(pwd)/rmv-lcd.py /usr/bin/rmv-lcd.py
fi
sudo cp ./config.json /etc/rmv-pi/
sudo cp ./rmv-lcd.service /etc/systemd/user/
systemctl --user enable rmv-lcd.service
systemctl --user restart rmv-lcd.service
