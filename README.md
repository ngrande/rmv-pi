# RMV-Pi
A Pi terminal to display the next trains for the train stations near you.

## Setup
To install everything simply call `./setup.sh` (note: this requires sudo rights)

It will install everything and start the service. Installtion includes:
+ link config.json into `/etc/rmv-lcd/`
+ link exec script to `/usr/bin/rmv-lcd.py`
+ copy rmv-lcd.service into `/etc/systemd/system/`
+ enable service
+ restart service

## Configuration
The script requires a configuration (pin layout, train stations, etc.).

An example:

    {
        "led_red": 19,
        "led_green": 12,
        "led_blue": 26,
        "lcd_rs": 25,
        "lcd_en": 24,
        "lcd_d4": 23,
        "lcd_d5": 17,
        "lcd_d6": 18,
        "lcd_d7": 22,
        "lcd_backlight": 13,
        "lcd_columns": 16,
        "lcd_rows": 2,
        
        "start_station": "Wiesenau",
        "main_dest": ["Hauptwache", "Hauptwache"],
        "sec_dest": ["Uni Campus Riedberg", "Riedberg"],
        
        "rmv_scr_path": "/home/pi/projects/rmv-terminal/rmv-terminal.py",

        "min_minutes": 3
    }
