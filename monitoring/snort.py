__author__ = 'lsh'

import os
import datetime


def get_cpu_and_mem():
    """
    Get CPU and Memory usage information with Linux command 'ps'
    :return: Dictionary containing CPU ('cpu') and memory ('mem') utilization as a relative value between 0 and 1
    :rtype: dict[str, float]
    """
    # get pids of snort
    pids = os.popen("pgrep snort").read()
    values = {"cpu": 0.0, "memory": 0.0}
    if pids:
        pid = pids.strip()
        comm = "ps -p " + str(pid) + " -o pmem,pcpu"
        info = os.popen(comm).read().split('\n')[1]
        tmp = info.strip().split(' ')
        if '' in tmp:
            tmp.remove('')
        values['cpu'] = round(float(tmp[-1])/100.,3)
        values['memory'] = round(float(tmp[-2])/100.,3)
    return values


def _parse_stats(log_file):
    with open(log_file) as f:
        lines = f.read().splitlines()
        # second line contains keys, first character of second line is a #
        second_line = lines[1][1:]
        keys = second_line.split(',')

        values = [0.]*len(keys)
        last_line = lines[-1]
        if last_line[0] != '#':
            values = map(float, last_line.split(','))
        return dict(zip(keys, values))


def get_traffic_stats(log_file):
    """
    Get traffic stats.
    :return: Dictionary containing pkt_drop_percent, alerts_per_second and kpackets_per_sec.realtime
    :rtype: dict[str, float]
    """
    all_stats = _parse_stats(log_file)
    desired_keys = ['pkt_drop_percent', 'alerts_per_second', 'kpackets_per_sec.realtime']
    return dict(zip(desired_keys, map(all_stats.get, desired_keys)))
