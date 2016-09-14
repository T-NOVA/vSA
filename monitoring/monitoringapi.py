import argparse
from influxdb import InfluxDBClient
import os

uuid_file = '/usr/local/etc/instance_uuid'
fixed_uuid = '03ed10fb-39d0-455e-bd5c-882552baaef0'

def get_uuid():
    if os.path.isfile(uuid_file):
        with open(uuid_file, 'r') as f:
            return f.readline().rstrip()
    else:
        return fixed_uuid

class MonitoringAPI(object):

    def __init__(self, host='monitoring', port=8086, username='stats_user', password='tnova', db_name='statsdb'):
        self.client = InfluxDBClient(host, port, username, password, db_name)


    def send_metric(self, name, value) :
        json_body = [
                {
                    "measurement": name,
                    "tags": {
                        "host": get_uuid()
                        },
                    "fields": {
                        "value": value
                        }
                    }
                ]
        self.client.write_points(json_body)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Send metrics to T-NOVA VIM infrastructure.')
    parser.add_argument('name', action="store")
    parser.add_argument('value', action="store")
    opts = parser.parse_args()
    shell = MonitoringAPI()
    shell.send_metric(opts.name, opts.value)
