#!/bin/sh
. ./cgi_lib.cgi

show_msg "Resetting System Configuration" /system_management.html 2000

factory_config_reset.sh > /dev/null
