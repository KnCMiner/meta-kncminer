#!/bin/sh
#set -x

killall -0 cgminer 2&> /dev/null
if [ $? = 0 ] ; then
    pid=`pidof cgminer`
    tasks=`ls /proc/$pid/task/|wc -l`
    if [ $tasks -gt 1 ] ; then
	proc_running="Running (pid="$pid")"
    else
	proc_running="Halted (Check Miner Settings)"
    fi
else
    proc_running="Stopped"
fi


> /tmp/mining_stats.$$

if [ "`echo $proc_running | grep Running`" != "" ] ; then
    
    data=`/usr/bin/api-cgminer -o summary | sed '
    s#|SUMMARY##g
    s#|##g
    s#%##g
    s# #_#g'`

    IFS=","
    set -- $data
    
    for d in $data ; do
	echo $d >> /tmp/mining_stats.$$
    done
    
    . /tmp/mining_stats.$$
    probe_time=`date -d @"$When"`
fi

sed '
s/#%#Status#%#/'"$proc_running"'/g
s/#%#time#%#/'"$probe_time"'/g
s/#%#hashrate#%#/'"$Work_Utility"'/g
s/#%#accepted#%#/'"$Accepted"'/g
s/#%#rejected#%#/'"$Rejected"'/g' < /www/tmpl/mining_stat.html_tmpl

rm /tmp/mining_stats.$$
