#!/usr/local/bin/php
<?php
    require_once('interfaces.inc');
    $lanif = get_real_interface('lan');
    $ifinfo_lan = pfsense_get_interface_stats($lanif);
    var_dump($ifinfo_lan);
?>
