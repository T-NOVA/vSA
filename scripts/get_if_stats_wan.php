#!/usr/local/bin/php
<?php
    require_once('interfaces.inc');
    $wanif = get_real_interface('wan');
    $ifinfo_wan = pfsense_get_interface_stats($wanif);
    var_dump($ifinfo_wan);
?>
