import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SERVICE_MAP = {
    'ds18b20': {
        'module': 'sensors.ds18b20',
        'class': 'DS18B20',
    },
}
