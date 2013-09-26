#!/bin/sh
. ./cgi_lib.cgi
error=false

IFS="&"
set -- $QUERY_STRING

for i in $@; do 
    IFS="="
    set -- $i
    if [ "$2" = "" ] ; then
	# error, all fields are mandatory
	error=true
	invalid_parameter=$1
	break
    elif [ "$1" = "url" ] ; then
	url=`urldecode "$2"`
    elif [ "$1" = "account" ] ; then
	account=`urldecode "$2"`
    elif [ "$1" = "password" ] ; then
	password=`urldecode "$2"`
    fi
done

if [ "$error" = "false" ] ; then
    sed -i 's#"url" :.*#"url" : "'${url}'"#g' /config/cgminer.conf
    sed -i 's#"user" :.*#"user" : "'${account}'"#g' /config/cgminer.conf
    sed -i 's#"pass" :.*#"pass" : "'${password}'"#g' /config/cgminer.conf
fi

if [ "$error" = "false" ] ; then
    /etc/init.d/miner_config.sh
    /etc/init.d/cgminer.sh restart > /dev/null
    show_apply_changes
else
    show_msg "Missing mandatory parameter \"$invalid_parameter\""
fi

exit 0
