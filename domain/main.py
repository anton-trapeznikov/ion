from settings import config
import importlib
import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser(description='Запуск доменных сервисов.')
    parser.add_argument('--service', metavar='service_name', dest='service',
                        type=str, required=True, help='Запускаемый сервис.')
    parser.add_argument('--entry', metavar='entry_id', dest='entry_id',
                        type=str, required=False, help='ID рабочей сущности.')

    options = parser.parse_args(argv)

    if options.service not in config.SERVICE_MAP:
        raise RuntimeError('%s service is unknown.' % options.service)

    service_class = getattr(
        importlib.import_module(
            config.SERVICE_MAP[options.service]['module']
        ),
        config.SERVICE_MAP[options.service]['class']
    )
    context = service_class(**vars(options))
    context.start()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
