#!/usr/bin/env python3

# pip install --upgrade rpi-lgpio
from RPi import GPIO
import logging
import time

# https://wiki.radxa.com/Penta_SATA_HAT
# Pin 8 connects to either Board pin 13 or 33
# GPIO27 = Board Pin 13 = GPIO4_C6 in Penta hat terminology         
# GPIO13 = Board Pin 33 = channel 1

def read_cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return int(f.read().strip()) / 1000.0

def determine_duty_cycle(cpu_temp):
    dc = 0
    if cpu_temp > 70:
        dc = 100
    elif cpu_temp > 60:
        dc = 80
    elif cpu_temp > 45:
        dc = 40
    elif cpu_temp > 35:
        dc = 20
    else:
        dc = 0
    return dc

def main_loop():
    pin_index = 13
    
    try:
        GPIO.setup(pin_index, GPIO.OUT, initial = 0)
        pwm = GPIO.PWM(pin_index, 25)
        pwm.start(80)

        while True:
            time.sleep(1.0)
            cpu_temp = read_cpu_temp()
            duty_cycle = determine_duty_cycle(cpu_temp)
            pwm.ChangeDutyCycle(duty_cycle)
    finally:
        GPIO.cleanup(pin_index)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(True)

    main_loop()
