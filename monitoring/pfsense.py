import subprocess

__author__ = 'hsi'

import re
import utils

#ARRAY_DUMP_REGEX = re.compile(r"\[\"(\w+)\"\]=>int\((\d+)\)")
ARRAY_DUMP_REGEX = re.compile(r"\'(\w+)\'=>int\((\d+)\)")
IOSTAT_REGEX = re.compile(r"\s+(\d+)")
MEMORY_REGEX = re.compile(r"(\d+)(M|G)")
HDD_REGEX = re.compile(r"(\d+)%")
LOAD_AVERAGE_REGEX =  re.compile(r"0\.\d+")


def get_traffic_stats(keys=('inerrs', 'outerrs', 'inbytes', 'outbytes', 'inpkts', 'outpkts', 'collisions')):
    """
    Gets bytes in/out, packets in/out, errors in/out and collisions in/out for the WAN and LAN interfaces.
    :return: Dictionary with keys wan_inbytes, wan_outbytes, wan_inpkts, wan_outpkts, wan_inerrs, wan_outerrs,
    wan_collisions, wan_inmcasts, wan_outmcasts, wan_inmcasts, wan_unsuppproto, wan_mtu.
    :rtype: dict[str, int]
    """
    if_stats_wan = subprocess.check_output("/home/tnova/tnova/scripts/get_if_stats_wan.php")
    if_stats_wan = if_stats_wan.replace('\n', '')
    if_stats_wan = if_stats_wan.replace(' ', '')
    stats_wan = dict(map(lambda e: (e[0], int(e[1])), ARRAY_DUMP_REGEX.findall(if_stats_wan)))
    stats_wan = utils.add_prefix_to_keys('wan_', utils.get_sub_dict(stats_wan, keys))

    if_stats_lan = subprocess.check_output("/home/tnova/tnova/scripts/get_if_stats_lan.php")
    if_stats_lan = if_stats_lan.replace('\n', '')
    if_stats_lan = if_stats_lan.replace(' ', '')
    stats_lan = dict(map(lambda e: (e[0], int(e[1])), ARRAY_DUMP_REGEX.findall(if_stats_lan)))
    stats_lan = utils.add_prefix_to_keys('lan_', utils.get_sub_dict(stats_lan, keys))

    stats_wan.update(stats_lan)
    return stats_wan

def get_system_stats():
    """
    Gets five metrics from get_stats.php, metrics: cpu_usage, mem_usage, dis_usage, uptime, pfstate
    :return: system_stats
    :rtype: dict
    """
    system_stats = dict()
    metrics = subprocess.check_output("/home/tnova/tnova/scripts/get_stats.php").split('\n')[-6:]
    system_stats['cpu'] = float(metrics[0])/100.
    system_stats['mem'] = float(metrics[1])/100.
    system_stats['dis'] = float(metrics[2])/100.
    system_stats['uptime'] = metrics[3]
    system_stats['pfstate'] = float(metrics[4])/100.
    load_avg = map(float, LOAD_AVERAGE_REGEX.findall(metrics[5]))
    load_avg = round(sum(load_avg)/len(load_avg), 2)
    system_stats['load_avg'] = load_avg
    return system_stats

