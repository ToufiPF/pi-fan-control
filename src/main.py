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


# Note: state default value is bound only once at function definition ;
# so consecutive calls will share the same state object
def determine_duty_cycle(config: Configuration, cpu_temp: float, state={}) -> int:
    """
    Given the CPU temperature in °C,
    returns the fan duty cycles from 0 to 100
    """
    if config.constant_duty_cycle is not None:
        logging.debug(f'config.constant_duty_cycle is set to {config.constant_duty_cycle}, returning.')
        return config.constant_duty_cycle

    if 'last_threshold' not in state:
        state['last_threshold'] = -float('inf')
        state['last_dc'] = None
        state['change_time'] = -float('inf')

    if state['last_dc'] is not None and cpu_temp < state['last_threshold'] and (time.time() - state['change_time']) < config.backoff_time:
        dc = state['last_dc']
        thres = state['last_threshold']
        logging.debug(f'CPU Temp: {cpu_temp:.1f}°C (below last_threshold={thres:.1f}°C, but backoff time is not elapsed) -> DC = {dc}')
        return dc

    duty_cycle = 0
    for (threshold, dc) in sorted(zip(config.temperature_thresholds, config.duty_cycles), key=itemgetter(0)):
        if cpu_temp >= threshold:
            duty_cycle = dc
            break

    if state['last_dc'] != duty_cycle:
        logging.info(f'CPU Temp: {cpu_temp:.1f}°C -> DC = {duty_cycle}')

    state['last_threshold'] = threshold
    state['last_dc'] = duty_cycle
    state['change_time'] = time.time()
    return duty_cycle



def main_loop(config: Configuration):
    i = 0
    with config.pwm_class(50) as pwm:
        while True:
            time.sleep(config.poll_interval)
            cpu_temp = read_cpu_temp()
            duty_cycle = determine_duty_cycle(config, cpu_temp)
            pwm.set_duty_cycle(duty_cycle)
            i += 1


if __name__ == '__main__':
    logging.basicConfig(level= logging.INFO)
    config = parse_config()
    main_loop(config)
