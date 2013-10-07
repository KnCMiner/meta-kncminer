#!/bin/sh
. ./cgi_lib.cgi

show_msg "Rebooting System (please wait 90 seconds)" index.html 60000

reboot

