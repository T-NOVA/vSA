#!/usr/local/bin/php
<?php
    require_once('includes/functions.inc.php');
    echo cpu_usage(), "\n";
    echo mem_usage(), "\n";
    echo disk_usage('/'), "\n";
    echo get_uptime(), "\n";
    echo get_pfstate(true), "\n";
    echo get_load_average();
?>
