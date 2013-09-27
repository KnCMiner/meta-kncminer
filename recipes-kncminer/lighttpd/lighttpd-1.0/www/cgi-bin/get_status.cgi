#!/bin/sh
. ./cgi_lib.cgi

killall -0 cgminer
if [ $? = 0 ] ; then
    sed '
s/#%#Color#%#/green/g
s/#%#Status#%#/Running/g' < /www/tmpl/index.html_tmpl > /www/pages/index.html
else
    sed '
s/#%#Color#%#/red/g
s/#%#Status#%#/Stopped/g' < /www/tmpl/index.html_tmpl > /www/pages/index.html
fi

show_msg "Checking status"


