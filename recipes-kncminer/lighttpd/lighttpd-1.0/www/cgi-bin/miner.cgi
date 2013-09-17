#!/bin/sh
. ./cgi_lib.cgi
error=false

IFS="&"
set -- $QUERY_STRING

> /tmp/miner.conf.$$
for i in $@; do 
    IFS="="
    set -- $i
    if [ "$2" = "" ] ; then
	# error, all fields are mandatory
	error=true
	invalid_parameter=$1
	break
    else
	echo $1=$2 >> /tmp/miner.conf.$$
    fi
done

if [ "$error" = "false" ] ; then
    mv /tmp/miner.conf.$$ /boot/knc_config/miner.conf
else
    rm /tmp/miner.conf.$$
fi

if [ "$error" = "false" ] ; then
    show_apply_changes
else
    echo "Content-type: text/html"
    echo ""
    
    echo '<html>'
    echo '<head>'
    echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
    echo '<title>NOK</title>'
    echo '</head>'
    echo '<body>'
    echo 'NOK'
    echo 'missing mandatory "'$invalid_parameter'" field'
    
    echo '</body>'
    echo '</html>'
 fi

#if [ "$error" = "false" ] ; then
#    /etc/init.d/cgminer.sh restart
#fi

exit 0
