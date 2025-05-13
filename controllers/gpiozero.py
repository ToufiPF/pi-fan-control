# pip install --upgrade gpiozero
from gpiozero import PWMLED

# GPIO13 = Board Pin 33

# Run `cat /sys/kernel/debug/pwm` to see hardware PWM state

# Add the following in /boot/firmware/config.txt :
# dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4
# This enables PWM on GPIO12 and GPIO13
# GPIO13 = PWM33 = PWM0_CHAN1

class GpioZeroPWM:
    """
    This class uses software PWM to control pin GPIO13 (=board pin 33)
    """
    def __init__(self, initial_duty_cycle: int):
        self.pwm = PWMLED('GPIO13', frequency=25)
        self.initial_duty_cycle = initial_duty_cycle

    def change_duty_cycle(self, duty_cycle: int):
        self.pwm.value = duty_cycle / 100

    def __enter__(self):
        self.pwm.value = self.initial_duty_cycle / 100
        self.pwm.on()

    def __exit__(self, exc_type, exc_value, traceback):
        self.pwm.off()
