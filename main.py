#!/usr/bin/env python3
import sys
import time
import logging
from config import read_config, Configuration
from operator import itemgetter

def read_cpu_temp() -> float:
    """
    Returns CPU temperature in °C
    """
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return int(f.read().strip()) / 1000.0


def determine_duty_cycle(config: Configuration, cpu_temp: float, verbose = False) -> int:
    """
    Given the CPU temperature in °C,
    returns the fan duty cycles from 0 to 100
    """
    if config.constant_duty_cycle is not None:
        if verbose:
            logging.info(f'config.constant_duty_cycle is set to {config.constant_duty_cycle}, returning.')
        return config.constant_duty_cycle

    duty_cycle = 0
    for (threshold, dc) in sorted(zip(config.temperature_thresholds, config.duty_cycles), key=itemgetter(0)):
        if cpu_temp >= threshold:
            duty_cycle = dc
            break

    if verbose:
        logging.info(f'CPU Temp: {cpu_temp:.1f}°C -> DC = {duty_cycle}')

    return duty_cycle


def main_loop(config: Configuration, pwmClass: type):
    i = 0
    with pwmClass(50) as pwm:
        while True:
            verbose = i % 10 == 0
            time.sleep(config.poll_interval)
            cpu_temp = read_cpu_temp()
            duty_cycle = determine_duty_cycle(config, cpu_temp, verbose=verbose)
            pwm.set_duty_cycle(duty_cycle)
            i += 1


if __name__ == '__main__':
    logging.basicConfig(level= logging.INFO)

    pwmClass = None
    requestedPwm = sys.argv[1] if len(sys.argv) >= 2 else 'pylgpio'
    config_path = sys.argv[2] if len(sys.argv) >= 3 else '/etc/raspberry-pi-fan-control.conf'
    config = read_config(config_path)

    match requestedPwm.lower():
        case 'pylgpio' | 'lgpio':
            from controllers.pylgpio import LgpioPWM
            pwmClass = LgpioPWM

        case 'gpiozero' | 'zero':
            from controllers.gpiozero import GpioZeroPWM
            pwmClass = GpioZeroPWM

        case 'hw' | 'rpihw' | 'hardware' | 'rpihardware':
            from controllers.rpihardwarepwm import HardwarePWM
            pwmClass = HardwarePWM
        case _:
            error = f'Unsupported requested PWM controller name "{requestedPwm}"'
            logging.error(error)
            raise ValueError(error)

    logging.info(f'Using controller "{requestedPwm}" ({pwmClass})')
    main_loop(config, pwmClass)
