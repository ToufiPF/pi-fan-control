#!/usr/bin/env python3

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

def main_loop():
    from controllers.pylgpio import LgpioPWM

    with LgpioPWM(80) as pwm:
        while True:
            time.sleep(1.0)
            cpu_temp = read_cpu_temp()
            duty_cycle = determine_duty_cycle(cpu_temp)
            pwm.set_duty_cycle(duty_cycle)

if __name__ == '__main__':
    main_loop()
