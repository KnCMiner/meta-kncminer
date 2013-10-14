#!/bin/sh
. ./cgi_lib.cgi

show_msg "Rebooting System <br>(please wait for 90 seconds)" / 90000

reboot.safe

