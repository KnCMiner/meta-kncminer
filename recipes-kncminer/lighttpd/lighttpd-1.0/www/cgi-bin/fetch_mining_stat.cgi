#!/bin/sh
#set -x

asic_stat_file=/var/run/stats.knc
if [ -f $asic_stat_file ] ; then
    i=1
    
    OIFS=$IFS
    IFS="="
    while read status ; do
	set -- $status
	if [ "$1" != "" ] ; then  
	    if [ "$2" != "OFF" ] ; then
		asic_status="${asic_status}ASIC slot #$i: $2 \&#x2103;<br>"
		i=`expr $i + 1`
	    else
		asic_status="${asic_status}ASIC slot #$i: -<br>"
		i=`expr $i + 1`
	    fi
	fi
	
    done <  $asic_stat_file
    IFS=$OIFS
fi


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


if [ "`echo $proc_running | grep Running`" != "" ] ; then
    data=`/usr/bin/api-cgminer -o`
    IFS=","
    set -- $data
    
    for d in $data ; do
	IFS="="
	set -- $d
	if [ "$1" = "When" ] ; then
	    probe_time=`date -d @"$2"`
	elif [ "$1" = "MHS av" ] ; then
	    hashrate=$2
	elif [ "$1" = "Accepted" ] ; then
	    accepted=$2
	elif [ "$1" = "Rejected" ] ; then
	    rejected=$2
	fi
    done
fi

sed '
s/#%#Status#%#/'"$proc_running"'/g
s/#%#time#%#/'"$probe_time"'/g
s/#%#hashrate#%#/'"$MHS_av"'/g
s/#%#accepted#%#/'"$Accepted"'/g
s/#%#rejected#%#/'"$Rejected"'/g
s/#%#ASIC_STATUS#%#/'"$asic_status"'/g' < /www/tmpl/mining_stat.html_tmpl
