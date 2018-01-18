from sensors.ds18b20 import DS18B20
#  import settings.config as config
import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser(description='Запуск доменных сервисов.')
    parser.add_argument('--service', metavar='service_name', dest='service',
                        type=str, required=True, help='Запускаемый сервис.')
    options = parser.parse_args(argv)

    if options.service.lower() == 'ds18b20':
        context = DS18B20()
        context.run()


if __name__ == '__main__':
    main(sys.argv[1:])
