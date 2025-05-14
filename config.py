from configparser import ConfigParser
import logging

class Configuration:
    def __init__(self):
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

def read_config(config_path: str) -> Configuration:
    """
    Reads and parses the Configuration at the given path
    """
    config = Configuration()
    try:
        defaults = Configuration()
        parser = ConfigParser()
        parser.read(config_path)

        config.constant_duty_cycle = parser.getint('fan', 'constant_duty_cycle', fallback= defaults.constant_duty_cycle)
        config.poll_interval = parser.getfloat('fan', 'poll_interval', fallback= defaults.poll_interval)
        config.duty_cycles = _parse_int_list(parser.get('fan', 'duty_cycles', fallback= _join_list(defaults.duty_cycles)))
        config.temperature_thresholds = _parse_int_list(parser.get('fan', 'temperature_thresholds', fallback= _join_list(defaults.temperature_thresholds)))

        logging.info(f'Successfully read config from "{config_path}"')
    except Exception as e:
        config = Configuration()
        logging.error(f'Error occured when loading configuration from "{config_path}". Falling back on defaults', e)

    logging.info('Configuration used:')
    width = 2 + max(len(key) for key in vars(config))
    for key, value in vars(config).items():
        logging.info(f'{key:>{width}s} = {value}')

    return config


def _join_list(list: list) -> str:
    return ",".join(str(x) for x in list)

def _parse_int_list(joined_list: str) -> list[int]:
    return list(int(x.strip()) for x in joined_list.split(','))
