#!/bin/sh
. /www/pages/cgi-bin/cgi_lib.cgi

usleep 100
killall -0 cgminer 2&> /dev/null

if [ $? = 0 ] ; then
    pid=`pidof cgminer`
    tasks=`ls /proc/$pid/task/|wc -l`
    if [ $tasks -gt 1 ] ; then
	sed '
s/#%#Color#%#/green/g
s/#%#Status#%#/Running (pid='"$pid"')/g' < /www/tmpl/index.html_tmpl > /www/pages/index.html
    else
    sed '
s/#%#Color#%#/red/g
s/#%#Status#%#/Halted (Check Miner Settings)/g' < /www/tmpl/index.html_tmpl > /www/pages/index.html
    fi
else
    sed '
s/#%#Color#%#/red/g
s/#%#Status#%#/Stopped/g' < /www/tmpl/index.html_tmpl > /www/pages/index.html
fi

show_msg "Checking status"


