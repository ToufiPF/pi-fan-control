# pip install --upgrade rpi_hardware_pwm
from rpi_hardware_pwm import HardwarePWM as RpiHwPWM

# Run `cat /sys/kernel/debug/pwm` to see hardware PWM state

# Add the following in /boot/firmware/config.txt :
# dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4
# This enables PWM on GPIO12 and GPIO13
# GPIO13 = PWM33 = PWM0_CHAN1

class HardwarePWM:
    """
    This class uses hardware PWM to control pin PWM33 (aka. GPIO13, aka. board pin 13)
    """
    def __init__(self, initial_duty_cycle: int):
        self.pwm = RpiHwPWM(pwm_channel=1, hz=25000, chip=0)
        self.initial_duty_cycle = initial_duty_cycle

    def set_duty_cycle(self, duty_cycle: int):
        self.pwm.change_duty_cycle(duty_cycle)

    def __enter__(self):
        self.pwm.start(self.initial_duty_cycle)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pwm.stop()
        self.pwm = None
