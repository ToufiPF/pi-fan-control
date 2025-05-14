#!/usr/bin/env python3
import sys
import time

def read_cpu_temp() -> float:
    """
    Returns CPU temperature in °C
    """
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return int(f.read().strip()) / 1000.0


def determine_duty_cycle(cpu_temp: float) -> int:
    """
    Given the CPU temperature in °C,
    returns the fan duty cycles from 0 to 100
    """
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


def main_loop(pwmClass: type):
    with pwmClass(50) as pwm:
        while True:
            time.sleep(5.0)
            cpu_temp = read_cpu_temp()
            duty_cycle = determine_duty_cycle(cpu_temp)
            print(f'CPU Temp: {cpu_temp:.1f}°C -> DC = {duty_cycle}')
            pwm.set_duty_cycle(duty_cycle)


if __name__ == '__main__':
    pwmClass = None
    requestedPwm = sys.argv[1] if len(sys.argv) >= 2 else 'pylgpio'

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
            raise ValueError(f'Unsupported requested PWM controller name "{requestedPwm}"')

    print(f'Using controller "{requestedPwm}" ({pwmClass})')
    main_loop(pwmClass)
