Virtual Security Appliance (vSA)
================================

SSH Access:

* `ssh -i /path/to/id_rsa tnova@vSA`


Configuration
-------------

### Pfsense

Configuration:
* `/conf/config.xml`
* remove `/tmp/config.cache`
* reload config by saving the "relevant" page (-> web configuration)

### Snort

Configuration:
* `/usr/local/etc/snort/snort.conf`
* `/etc/rc.conf.local`

* `ipvar HOME_NET [192.168.1.0/24]`
* `ipvar EXTERNAL_NET !$HOME_NET`

Log: `/var/log/snort/merged.log.xxxxxxxxxx`


vSA Logic
---------

### Repository

The vSA logic resides in a Git repository that is located at 
`/home/tnova/tnova`. The branch `production` has to be used.

To pull or push updates, first copy the `resolv.conf` file in `/home/tnova` to
`/etc/resolv.conf`.

### Controlling the vSA

The vSA can be started/stopped/restarted with the command: 
`sudo python /home/tnova/tnova/vsa/vsa.py <command>` where `<command>` is either
`start`, `stop` or `restart`.

### configuring monitoring ###

1.Install "collectd5" in vSA using command "pkg install collectd5",then run command "rehash"

2.Add collectd_enable="YES" to file /etc/rc.conf.local

3.Change /usr/local/etc/collectd.conf      # collectd.conf is backed up in /home/tnova/tnova/conf

4.Add /usr/local/etc/rc.d/update_uuid.sh    # It gets instance uuid, stores it to a file, updates and restarts collectd, adds our local DNS on top of /etc/resolv.conf.  update_uuid.sh is backed up in /home/tnova/tnova/conf

