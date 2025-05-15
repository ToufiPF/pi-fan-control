# pip install --upgrade rpi-lgpio
from RPi import GPIO

# https://wiki.radxa.com/Penta_SATA_HAT
# Pin 8 connects to either Board pin 13 or 33
# GPIO27 = Board13 = GPIO27 = GPIO4_C6 in Penta hat terminology
# GPIO13 = Board33 = chann1 = PWM_33   in Penta hat terminology

# Add the following in /boot/firmware/config.txt :
# dtoverlay=w1-gpio

class LgpioPWM:
    """
    This class uses software PWM to control board pin 13
    """
    def __init__(self, initial_duty_cycle: int):
        self.pin = 13
        self.initial_duty_cycle = initial_duty_cycle

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(True)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 25)

    def set_duty_cycle(self, duty_cycle: int):
        self.pwm.ChangeDutyCycle(duty_cycle)

    def __enter__(self):
        self.pwm.start(self.initial_duty_cycle)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pwm.stop()
        self.pwm = None
        GPIO.cleanup(self.pin)
