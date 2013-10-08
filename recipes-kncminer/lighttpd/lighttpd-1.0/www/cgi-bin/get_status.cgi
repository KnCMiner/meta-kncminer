#!/bin/sh

cat  /www/tmpl/index.html_tmpl
exit 0

# to be removed
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

usleep 100
killall -0 cgminer 2&> /dev/null

if [ $? = 0 ] ; then
    pid=`pidof cgminer`
    tasks=`ls /proc/$pid/task/|wc -l`
    if [ $tasks -gt 1 ] ; then
	sed '
s/#%#Color#%#/green/g
s/#%#ASIC_STATUS#%#/'"$asic_status"'/g
s/#%#Status#%#/Running (pid='"$pid"')/g' < /www/tmpl/index.html_tmpl
    else
    sed '
s/#%#Color#%#/red/g
s/#%#ASIC_STATUS#%#/'"$asic_status"'/g
s/#%#Status#%#/Halted (Check Miner Settings)/g' < /www/tmpl/index.html_tmpl
    fi
else
    sed '
s/#%#Color#%#/red/g
s/#%#ASIC_STATUS#%#/'"$asic_status"'/g
s/#%#Status#%#/Stopped/g' < /www/tmpl/index.html_tmpl
fi
