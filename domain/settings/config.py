import json
import sys
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

json_config_file = os.path.join(BASE_DIR, 'settings', 'config.json')
if os.path.exists(json_config_file):
    with open(json_config_file) as f:
        json_config = json.loads(f.read())
        for param, value in json_config.items():
            setattr(sys.modules[__name__], param, value)

CHANNEL_MAP = {
    'ds18b20': 'temperature',
}

SERVICE_MAP = {
    'ds18b20': {
        'module': 'sensors.ds18b20',
        'class': 'DS18B20',
    },
    'mq-broker': {
        'module': 'service.broker',
        'class': 'MQBroker',
    },
}

REDIS_KEY = {
    'ds18b20_value': 'ion:ds18b20::',
    'ds18b20_timestamp': 'ion:ds18b20::ts::',
    'ds18b20_ids': 'ion:ds18b20::list'
}
