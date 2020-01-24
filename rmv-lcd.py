#!/usr/bin/env python3

import os
import sys
import time
import subprocess
import json

import RPi.GPIO as GPIO

import Adafruit_CharLCD as LCD

config = {}
with open(os.path.join("/etc", "rmv-pi", "config.json"), "rb") as f:
    config = json.load(f)

# led config
led_red = config["led_red"]
led_green = config["led_green"]
led_blue = config["led_blue"]

# lcd config
lcd_rs        = config["lcd_rs"]
lcd_en        = config["lcd_en"]
lcd_d4        = config["lcd_d4"]
lcd_d5        = config["lcd_d5"]
lcd_d6        = config["lcd_d6"]
lcd_d7        = config["lcd_d7"]
lcd_backlight = config["lcd_backlight"]
lcd_columns = config["lcd_columns"]
lcd_rows = config["lcd_rows"]

start_station = config["start_station"]
main_dest = config["main_dest"]
sec_dest =  config["sec_dest"]

rmv_scr_path = config["rmv_scr_path"]

min_minutes = config["min_minutes"]

script_train_cmd = "{} {} --direction $TO$ --i3 --duration 360 --threshold {} --no-info".format(rmv_scr_path, start_station, min_minutes)
script_info_cmd = "{} {} --direction $TO$ --info-min-category 3".format(rmv_scr_path, start_station)


def update_info(red, green, blue):
    cmd = script_info_cmd.replace("$TO$", main_dest[0])
    infos = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8').split("\n")

    levels = set()
    txt = None
    for i, line in enumerate(infos):
        if "INFO [" in line:
            level = line.replace("INFO [", "").replace("]", "")
            level = int(level)
            levels.add(level)
            if level == 1 and len(infos) > i + 1:
                txt = infos[i + 1]

    for pwm in [red, green, blue]:
        # reset
        pwm.ChangeDutyCycle(0)
    if 1 in levels:
        # RED
        red.ChangeDutyCycle(15)
    elif 2 in levels:
        # orange
        red.ChangeDutyCycle(15)
        green.ChangeDutyCycle(0.5)
        blue.ChangeDutyCycle(0)
    elif 3 in levels:
        # yellow
        red.ChangeDutyCycle(15)
        green.ChangeDutyCycle(3)
        blue.ChangeDutyCycle(0)
    else:
        # green
        green.ChangeDutyCycle(0.2)

    return txt


def run(lcd, red, green, blue):
    lcd.clear()
    blue.ChangeDutyCycle(5)
    lcd.message("booting...")

    while True:
        new_msg = ""
        for dest, alias in [main_dest, sec_dest]:
            dest = dest.replace(" ", r"\ ")
            msg = subprocess.check_output(script_train_cmd.replace("$TO$", dest), shell=True).decode('utf-8')
            msg = msg.replace("\n", "")
            if len(alias) > 8:
                alias = alias[:8]
            new_msg += "{} {}\n".format(alias, msg)

        new_msg = new_msg[:-1]

        # display times
        lcd.clear()
        lcd.message(new_msg)
        txt = update_info(red, green, blue)

        # TODO display txt

def setup_led(pin):
    GPIO.setup(pin, GPIO.OUT)  # Set GPIO pin 12 to output mode.
    pwm = GPIO.PWM(pin, 100)   # Initialize PWM on pwmPin 100Hz frequency

    dc=0                               # set dc variable to 0 for 0%
    pwm.start(dc)                      # Start PWM with 0% duty cycle
    return pwm


if __name__ == '__main__':
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight, enable_pwm=True, initial_backlight=0.3, invert_polarity=False)

    red = setup_led(led_red)
    green = setup_led(led_green)
    blue = setup_led(led_blue)

 #   while True:
 #       i = input("R,G,B: ")
 #       r, g, b = i.split()
 #       red.ChangeDutyCycle(float(r))
 #       green.ChangeDutyCycle(float(g))
 #       blue.ChangeDutyCycle(float(b))

    run(lcd, red, green, blue)

    for pwm in [red, green, blue]:
        pwm.stop()
    GPIO.cleanup()


#  vim: tabstop=4 shiftwidth=4 noexpandtab
