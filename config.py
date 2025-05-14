from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
import logging

class Configuration:
    def __init__(self):
        self.pwm_controller: str = None
        """ Name of the PWM controller that should be used """

        self.pwm_class: type = None
        """ Type PWM controller that should be used (based on self.pwm_controller) """

        self.poll_interval: float = 5
        """ Interval in seconds between each round of polling temperature/change of DC """

        self.duty_cycles: list[int] = [100, 80, 50, 25]
        """
        List of N target DCs, IN DECREASING ORDER, where N is the number of temperature thresholds, IN DECREASING ORDER.
        Values range from 0 (off) to 100 (fully on).

        DC[i] is chosen when i is the smallest integer s.t. Threshold[i] <= cpu_temp.
        If all thresholds are > cpu_temp, the DC will be 0.
        """

        self.temperature_thresholds: list[int] = [70, 60, 45, 35]
        """
        List of N temperature thresholds in °C, IN DECREASING ORDER.
        Usual values are from 20°C to 75°C (starting to get too hot).

        DC[i] is chosen when i is the smallest integer s.t. Threshold[i] <= cpu_temp
        """

        self.constant_duty_cycle: int | None = None
        """ Optional DC that overrides the DC computed from the CPU temperature """


def parse_config() -> Configuration:
    """
    Reads and parses the Configuration
    """
    namespace = _parse_sysargv()
    config = _parse_config_file(namespace.config_path)

    config.pwm_controller = (namespace.pwm_controller or config.pwm_controller or 'lgpio').lower()
    config.pwm_class = _load_pwm_class(config.pwm_controller)

    logging.info('Configuration used:')
    width = 2 + max(len(key) for key in vars(config))
    for key, value in vars(config).items():
        logging.info(f'{key:>{width}s} = {value}')

    return config


def _parse_sysargv() -> Namespace:
    parser = ArgumentParser(add_help= False)
    parser.add_argument('--config_path', '--config', '-c',
                        type=str,
                        default='/etc/pi-fan-control.conf',
                        help='Path to the configuration file of this program')
    parser.add_argument('--pwm_controller', '--pwm', '-p',
                        type=str,
                        default=None,
                        help='''
                             Name of the PWM controller to use.
                             Supported values are:
                             - 'pylgpio' or 'lgpio': uses rpi-lgpio library
                             - 'gpiozero' or 'zero': uses gpiozero library
                             - 'rpihardware' or 'hardware' or 'hw': uses rpi_hardware_pwm library
                             ''')
    parser.add_argument('--help', '-h', '-?',
                        action='help',
                        help='Displays this message and exits.')
    return parser.parse_args()


def _parse_config_file(config_path: str) -> Configuration:
    try:
        config = Configuration()
        defaults = Configuration()
        parser = ConfigParser()
        parser.read(config_path)

        config.pwm_controller = parser.get('fan', 'pwm_controller', fallback= defaults.pwm_controller)
        config.constant_duty_cycle = parser.getint('fan', 'constant_duty_cycle', fallback= defaults.constant_duty_cycle)
        config.poll_interval = parser.getfloat('fan', 'poll_interval', fallback= defaults.poll_interval)
        config.duty_cycles = _parse_int_list(parser.get('fan', 'duty_cycles', fallback= _join_list(defaults.duty_cycles)))
        config.temperature_thresholds = _parse_int_list(parser.get('fan', 'temperature_thresholds', fallback= _join_list(defaults.temperature_thresholds)))

        logging.info(f'Successfully read config from "{config_path}"')
        return config
    except Exception as e:
        logging.error(f'Error occured when loading configuration from "{config_path}". Falling back on defaults', e)
        return Configuration()


def _load_pwm_class(pwm_name: str) -> type:
    match pwm_name:
        case 'pylgpio' | 'lgpio':
            from controllers.pylgpio import LgpioPWM
            return LgpioPWM

        case 'gpiozero' | 'zero':
            from controllers.gpiozero import GpioZeroPWM
            return GpioZeroPWM

        case 'rpihardware' | 'hardware' | 'hw':
            from controllers.rpihardwarepwm import HardwarePWM
            return HardwarePWM

        case _:
            error = f'Unsupported requested PWM controller name "{pwm_name}"'
            logging.error(error)
            raise ValueError(error)


def _join_list(list: list) -> str:
    return ",".join(str(x) for x in list)

def _parse_int_list(joined_list: str) -> list[int]:
    return list(int(x.strip()) for x in joined_list.split(','))
