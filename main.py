#!/usr/bin/env python3
import time
import logging
from operator import itemgetter
from config import parse_config, Configuration

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


def main_loop(config: Configuration):
    i = 0
    with config.pwm_class(50) as pwm:
        while True:
            verbose = i % 10 == 0
            time.sleep(config.poll_interval)
            cpu_temp = read_cpu_temp()
            duty_cycle = determine_duty_cycle(config, cpu_temp, verbose=verbose)
            pwm.set_duty_cycle(duty_cycle)
            i += 1


if __name__ == '__main__':
    logging.basicConfig(level= logging.INFO)
    config = parse_config()
    main_loop(config)
