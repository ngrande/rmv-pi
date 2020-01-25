#!/bin/bash

tdir="/etc/rmv-lcd"
if [ ! -h /usr/bin/rmv-lcd.py ]; then
	sudo ln -s $(pwd)/rmv-lcd.py /usr/bin/rmv-lcd.py
fi
if [ ! -d $tdir ]; then
	sudo mkdir -p $tdir
fi
if [ ! -h $tdir/config.json ]; then
	sudo ln -s $(pwd)/config.json $tdir/config.json
fi
sudo cp ./rmv-lcd.service /etc/systemd/system/
sudo systemctl enable rmv-lcd.service
sudo systemctl restart rmv-lcd.service
