# pip install --upgrade gpiozero
from gpiozero import PWMOutputDevice

# https://wiki.radxa.com/Penta_SATA_HAT
# Pin 8 connects to either Board pin 13 or 33
# GPIO27 = Board13 = GPIO27 = GPIO4_C6 in Penta hat terminology
# GPIO13 = Board33 = chann1 = PWM_33   in Penta hat terminology

# Add the following in /boot/firmware/config.txt :
# dtoverlay=w1-gpio

class GpioZeroPWM:
    """
    This class uses software PWM to control pin BOARD13 (aka. GPIO27)
    """
    def __init__(self, initial_duty_cycle: int):
        self.pwm = PWMOutputDevice('BOARD13', frequency=25)
        self.initial_duty_cycle = initial_duty_cycle

    def set_duty_cycle(self, duty_cycle: int):
        self.pwm.value = duty_cycle / 100

    def __enter__(self):
        self.pwm.value = self.initial_duty_cycle / 100
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pwm.off()
        self.pwm = None
