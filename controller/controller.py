from idstools import unified2, maps
import os
import subprocess
import logging
import time

VERSION = "3.3"
CONTROLLER_LOG_FILE = "/var/log/vsa-controller"
LOGGER_NAME = "vsa-controller"
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s: %(message)s"


class Controller(object):

    def __init__(self, logger, snort_log_dir="/var/log/snort/snort_vtnet08905/", snort_classification_conf="/usr/local/etc/snort/classification.config", interface='wan'):
        """
        Creates a new controller
        :param logger: Logger to use
        :param snort_log_dir: Directory of the snort unified 2 log files
        :param snort_classification_conf: Classification mapping config file
        :param interface: Interface name to use for blocking sources
        :return: New controller object
        """
        self.logger = logger

        # get the most recent snort log file
        #log_file = sorted(os.listdir(snort_log_dir), reverse=True)[0]
        self.log_file = snort_log_dir + "alert"
        logger.info('Using snort log file: %s' % self.log_file)
        #self.event_reader = unified2.SpoolEventReader(snort_log_dir, log_file, follow=True)
        #self.classification_map = maps.ClassificationMap(open(snort_classification_conf, 'r'))
        self.interface = interface

    def create_fw_rule(self, interface, ip_to_block):
        """
        Creates a firewall rule for 'interface' to block traffic from 'ip_to_block'
        :param interface: Interface name
        :type interface: str
        :param ip_to_block: IP address that should be blocked
        :type ip_to_block: str
        """
        self.logger.info("Blocking {0:s} on interface {1:s}".format(ip_to_block, interface))
        ret_code = subprocess.call(['easyrule', 'block', interface, ip_to_block])
        if ret_code == 1:
            self.logger.error('Failed to create blocking rule')

    def monitor_events(self):
        """
        Starts event monitoring.
        """
        alert_strings = ("(portscan) TCP Portscan", "ET SCAN Nmap Scripting Engine User-Agent Detected", "(portscan) TCP Filtered Portscan","ET SCAN Potential","ET POLICY Suspicious inbound")
       # for event in self.event_reader:
            #if event['priority'] <= 2:
            #    self.create_fw_rule(self.interface, event['source-ip'])
        with open(self.log_file, 'r') as f:
            #last_pos = f.tell()
            data = f.readlines()
            last_pos = f.tell()
            while True:
                f.seek(last_pos)
                new_data = f.readlines()
                for row in new_data:
                    if any(s in row for s in alert_strings):
                    #if '(portscan) TCP Portscan' in row:
                        source_ip = row.split(',')[6]
                    #    print source_ip
                         self.create_fw_rule(self.interface, source_ip)
                last_pos = f.tell()
                time.sleep(10)

def main():
    # set up logging
    # log to file
    logger = logging.getLogger(LOGGER_NAME)
    file_log = logging.FileHandler(CONTROLLER_LOG_FILE)
    log_level = logging.DEBUG
    logger.setLevel(log_level)
    file_log.setLevel(log_level)
    formatter = logging.Formatter(LOG_FORMAT)
    file_log.setFormatter(formatter)
    logger.addHandler(file_log)

    controller = Controller(logger)
    controller.monitor_events()


if __name__ == "__main__":
    main()
