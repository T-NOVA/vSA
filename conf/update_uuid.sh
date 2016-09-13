#!/bin/sh
# This script updates the UUID file and collectd and then restarts collectd
# Current requirements are curl and sed

uuid_file='/usr/local/etc/instance_uuid'

cr="
"

# Get UUID
uuid="$(curl -s http://169.254.169.254/openstack/latest/meta_data.json | sed -e 's/.*"uuid": "//; s/".*//')"

# Generate UUID file
touch $uuid_file
echo $uuid > $uuid_file

# Update and restart collectd
sed -i '' "s/^Hostname.*/Hostname \"$uuid\"/" /usr/local/etc/collectd.conf
service collectd restart


# Hack to prepend local DNS
sed -i '' "1s/^/nameserver 10.30.0.11\\${cr}/" /etc/resolv.conf


/usr/bin/touch /var/log/`/bin/date "+%H-%M-%S"`-try_to_call_tenor.log
echo "Reading /etc/tenor.cfg config file ..."
. /etc/tenor.cfg
echo "Config for the tenor_url: $tenor_url"
output=$(curl -X POST $tenor_url -d 'info')
echo $output > /var/log/tenor.response
echo "curl -X POST done to Tenor $output."


exit 0
