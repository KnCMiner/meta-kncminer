#!/bin/sh
. ./cgi_lib.cgi

show_msg "Rebooting System (please wait for 90 seconds)" index.html 90000

reboot.safe

