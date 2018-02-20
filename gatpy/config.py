import configparser
import os

DEFAULT_DATA_DIR = os.path.join(os.path.abspath(os.sep), 'GatPy', 'data')

config = configparser.ConfigParser()
config.read('gatpy.ini')


def get_data_dir():
    if 'Paths' in config.sections():
        result = config['Paths'].get('data_dir', DEFAULT_DATA_DIR)
    else:
        result = DEFAULT_DATA_DIR

    os.makedirs(os.path.join(result, 'log'), exist_ok=True)
    os.makedirs(os.path.join(result, 'raw'), exist_ok=True)
    os.makedirs(os.path.join(result, 'proc'), exist_ok=True)

    return result
