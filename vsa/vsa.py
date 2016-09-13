import os
import subprocess
import argparse
import logging
import pickle
import time

VSA_LOG_FILE = "/var/log/vsa"
LOGGER_NAME = "vsa"
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s: %(message)s"
PID_FILENAME = "/home/tnova/tnova/vsa/.vsa-pids"


def start(logger):
    logger.info('Starting vSA')

    # --- start snort
    #ret_code = subprocess.call(['service', 'snort', 'start'])
    #if ret_code == 1:
    #    logger.error('Failed to start Snort')

    # wait a little for snort to start, it takes some time until the snort log file is created
    # when the controller is started too fast, it will therefore use an old log file, because the new is not there, yet
    #time.sleep(5)

    # --- start controller
    controller_subproc = subprocess.Popen(['python', '/home/tnova/tnova/controller/controller.py'])

    # --- start monitoring
    monitoring_subproc = subprocess.Popen(['python', '/home/tnova/tnova/monitoring/monitoring.py'])

    pids_dict = {'controller': controller_subproc.pid, 'monitoring': monitoring_subproc.pid if monitoring_subproc else -1}
    pid_file = file(PID_FILENAME, mode='w')
    pickle.dump(pids_dict, pid_file)

    logger.info('Start completed')


def stop(logger):
    logger.info('Stopping vSA')

    # --- stop snort
    #ret_code = subprocess.call(['service', 'snort', 'stop'])
    #if ret_code == 1:
        #logger.error('Failed to stop Snort')

    if os.path.isfile(PID_FILENAME):
        pid_file = file(PID_FILENAME, mode='r')
        pids_dict = pickle.load(pid_file)

        # --- stop controller
        subprocess.call(['kill', str(pids_dict['controller'])])

        # --- stop monitoring
        if pids_dict['monitoring'] != -1:
            subprocess.call(['kill', str(pids_dict['monitoring'])])

        subprocess.call(['rm', PID_FILENAME])

    logger.info('Stop completed')


def main():
    # define arguments
    # single obligatory argument 'command' controlling the vSA
    # optional argument controlling the log level
    parser = argparse.ArgumentParser(description='Control this virtual security appliance (vSA).')
    parser.add_argument('command', type=str, help='command to either start/stop/restart the vSA')
    parser.add_argument('-d', '--debug', action='store_true', help='sets log level to debug')
    parsed_args = parser.parse_args()

    # set up logging
    # logging to file, switching between INFO and DEBUG log level can be controlled with --debug switch
    logger = logging.getLogger(LOGGER_NAME)
    file_log = logging.FileHandler(VSA_LOG_FILE)
    log_level = logging.DEBUG if parsed_args.debug else logging.INFO
    logger.setLevel(log_level)
    file_log.setLevel(log_level)
    formatter = logging.Formatter(LOG_FORMAT)
    file_log.setFormatter(formatter)
    logger.addHandler(file_log)

    if parsed_args.command == 'start':
        start(logger)
    elif parsed_args.command == 'stop':
        stop(logger)
    elif parsed_args.command == 'restart':
        start(logger)
        stop(logger)


if __name__ == "__main__":
    main()
