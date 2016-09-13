__author__ = 'lsh'


import pfsense
from monitoringapi import MonitoringAPI
import time
from bs4 import BeautifulSoup
import snort
import utils

SNORT_LOG_FILE = '/var/log/snort/snort.stats'

# send every 10 seconds metrics about pfsense and snort to monitoring host
def main():

    while(True):
        pfsense_stats = dict()
        pfsense_stats.update(pfsense.get_system_stats())
        pfsense_stats.update(pfsense.get_traffic_stats())

        snort_stats = snort.get_cpu_and_mem()
        snort_stats.update(snort.get_traffic_stats(SNORT_LOG_FILE))

        pfsense_stats = utils.add_prefix_to_keys('pfsense_', pfsense_stats)
        snort_stats = utils.add_prefix_to_keys('snort_', snort_stats)

        vsa_stats = dict()
        vsa_stats.update(pfsense_stats)
        vsa_stats.update(snort_stats)
        vsa_stats = utils.add_prefix_to_keys('vsa_', vsa_stats)

        # send data
        monitoring = MonitoringAPI()
        for k, v in vsa_stats.iteritems():
            monitoring.send_metric(k, v)

        time.sleep(10)

if __name__ == "__main__":
    main()
