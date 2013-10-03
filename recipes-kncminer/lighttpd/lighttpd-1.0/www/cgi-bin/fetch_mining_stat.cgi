#!/bin/sh
#set -x

killall -0 cgminer
if [ $? = 0 ] ; then
    proc_running="Running"
else
    proc_running="Stopped"
fi

> /tmp/x

if [ "$proc_running" = "Running" ] ; then
    
    data=`/usr/bin/api-cgminer -o summary | sed '
    s#|SUMMARY##g
    s#|##g
    s#%##g
    s# #_#g'`

    IFS=","
    set -- $data
    
    for d in $data ; do
	echo $d >> /tmp/x
    done
    
    . /tmp/x
    probe_time=`date -d @"$When"`
fi

sed '
s/#%#Status#%#/'"$proc_running"'/g
s/#%#time#%#/'"$probe_time"'/g
s/#%#hashrate#%#/'"$Work_Utility"'/g
s/#%#accepted#%#/'"$Accepted"'/g
s/#%#rejected#%#/'"$Rejected"'/g' < /www/tmpl/mining_stat.html_tmpl

rm /tmp/x
