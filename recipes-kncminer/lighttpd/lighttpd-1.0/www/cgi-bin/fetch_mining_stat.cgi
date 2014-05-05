#!/bin/sh
#set -x

asic_status="<table border=\"1\">"

asic_stat_file=/var/run/stats.knc
if [ -f $asic_stat_file ] ; then
    i=1
    
    OIFS=$IFS
    IFS="="
    while read status ; do
	set -- $status
	if [ "$1" != "" ] ; then  
	    if [ "$2" != "OFF" ] ; then
		asic_status="${asic_status}<tr><td>ASIC slot #$i</td><td>$2 \&#x2103;</td></tr>"
		i=`expr $i + 1`
	    else
		asic_status="${asic_status}<tr><td>ASIC slot #$i</td><td>-</td></tr>"
		i=`expr $i + 1`
	    fi
	fi
	
    done <  $asic_stat_file
    IFS=$OIFS
else
    for line in 1 2 3 4 5 6 ; do
	asic_status="${asic_status}<tr><td>ASIC slot #$i</td><td>-</td></tr>"
    done
fi

asic_status="${asic_status}</table>"

appname=
showname=
killall -0 cgminer 2&> /dev/null
if [ $? = 0 ] ; then
	appname=cgminer
	showname=CGMiner
else
	killall -0 bfgminer 2&> /dev/null
	if [ $? = 0 ] ; then
		appname=bfgminer
		showname=BFGMiner
	fi
fi
if [ "x$appname" != "x" ] ; then
    pid=`pidof $appname`
    tasks=`ls /proc/$pid/task/|wc -l`
    if [ $tasks -gt 1 ] ; then
	proc_running="Running $showname (pid="$pid")"
    else
	proc_running="Halted (Check Miner Settings)"
    fi
else
    proc_running="Stopped"
fi


if [ "`echo $proc_running | grep Running`" != "" ] ; then
    data=`/usr/bin/api-cgminer -o`
    
    # check that connect to miner was ok
    if [ "$data" = "Socket connect failed: Connection refused" ] ; then
	proc_running="Running (Connect to Miner API failed)"
	break
    fi

    IFS=","
    set -- $data
    
    for d in $data ; do
	IFS="="
	set -- $d
	if [ "$1" = "When" ] ; then
	    probe_time=`date -d @"$2"`
	elif [ "$1" = "MHS 1m" ] ; then
            hashrate="`expr ${2/.*} / 1000` Gh/s"
	elif [ "$1" = "Work Utility" ] ; then
	    work_utility=${2/.*}
	elif [ "$1" = "Difficulty Accepted" ] ; then
	    difficulty_accepted=${2/.*}
	fi
    done
fi

sed '
s/#%#Status#%#/'"$proc_running"'/g
s/#%#time#%#/'"$probe_time"'/g
s!#%#hashrate#%#!'"$hashrate"'!g
s/#%#workUtility#%#/'"$work_utility"'/g
s/#%#difficultyAccepted#%#/'"$difficulty_accepted"'/g
s!#%#ASIC_STATUS#%#!'"$asic_status"'!g' < /www/tmpl/mining_stat.html_tmpl
