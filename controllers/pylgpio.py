# pip install --upgrade rpi-lgpio
from RPi import GPIO

# https://wiki.radxa.com/Penta_SATA_HAT
# Pin 8 connects to either Board pin 13 or 33
# GPIO27 = Board Pin 13 = GPIO4_C6 in Penta hat terminology         
# GPIO13 = Board Pin 33 = channel 1

# Add the following in /boot/firmware/config.txt :
# dtoverlay=w1-gpio

class LgpioPWM:
    """
    This class uses software PWM to control board pin 13
    """
    def __init__(self, initial_duty_cycle: int):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(True)

        self.pin = 13
        self.pwm = GPIO.PWM(self.pin, 25)
        self.initial_duty_cycle = initial_duty_cycle

    def set_duty_cycle(self, duty_cycle: int):
        self.pwm.ChangeDutyCycle(duty_cycle)

    def __enter__(self):
        self.pwm.start(self.initial_duty_cycle)

    def __exit__(self, exc_type, exc_value, traceback):
        self.pwm.stop()
        GPIO.cleanup(self.pin)
