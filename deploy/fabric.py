from config_patterns import patterns
import glob
import sys
import os

UNSUCCESS_EXIT_CODE = 1

try:
    import conf
except ImportError:
    print('Error: deploy/conf.py not found or not valid.')
    sys.exit(UNSUCCESS_EXIT_CODE)


class Fabric(object):
    def __init__(self):
        self._workdir = conf.WORK_DIR
        self._python = conf.PYTHON_PATH
        self._user = conf.USER
        self._user_group = conf.USER_GROUP
        self._log_dir = '/var/log/ion/'
        self._supervisor_config_dir = '/etc/supervisor/conf.d'
        self.__check_requirements()
        self.__make_directories()

    def __check_requirements(self):
        errors = []
        if os.geteuid() != 0:
            errors.append('Error: %s must be run as root.' % __file__)

        if not os.path.exists(self._supervisor_config_dir):
            errors.append('Error: supervisor not found.')

        if errors:
            print('\n'.join(errors))
            sys.exit(UNSUCCESS_EXIT_CODE)

    def __make_directories(self):
        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)

    def __remove_old_supervisor_config(self, filename_pattern='ion-*'):
        config_filename_pattern = os.path.join(
            self._supervisor_config_dir,
            filename_pattern
        )

        for old_config_file in glob.glob(config_filename_pattern):
            os.remove(old_config_file)

    def make_ds18b20_daemons(self):
        self.__remove_old_supervisor_config(filename_pattern='ion-ds18b20-*')

        sensors = []
        ds18b20_directory_pattern = '/sys/bus/w1/devices/28-*'
        for directory in glob.glob(ds18b20_directory_pattern):
            sensor_slave_file = os.path.join(directory, 'w1_slave')
            if os.path.isdir(directory) and os.path.exists(sensor_slave_file):
                sensors.append(directory.split('/')[-1])

        for sensor_id in sensors:
            stdout_log = os.path.join(
                self._log_dir,
                'supervisor-ds18b20-%s-stdout.log' % sensor_id
            )
            self.touch_file(stdout_log)

            stderr_log = os.path.join(
                self._log_dir,
                'supervisor-ds18b20-%s-stderr.log' % sensor_id
            )
            self.touch_file(stderr_log)

            command = '%s %s --sensor=%s' % (
                self._python,
                os.path.join(self._workdir, 'domain/ds18b20.py'),
                sensor_id,
            )

            config = patterns['supervisor'].format(**{
                'daemon_name': 'ion-ds18b20-%s' % sensor_id,
                'directory': self._workdir,
                'exec_command': command,
                'user': self._user,
                'user_group': self._user_group,
                'stdout_logfile': stdout_log,
                'stderr_logfile': stderr_log,
            })

            output_file = os.path.join(
                self._supervisor_config_dir,
                'ion-ds18b20-%s.conf' % sensor_id
            )
            with open(output_file, 'w') as config_file:
                config_file.write(config)

        print('DS18B20: Done.')

    def touch_file(self, path):
        os.system('touch %s' % path)

    def build_all(self):
        self.make_ds18b20_daemons()


fabric = Fabric()
fabric.build_all()
