#!/bin/sh
. ./cgi_lib.cgi

show_msg "Rebooting System" index.html
sleep 1

reboot.safe

