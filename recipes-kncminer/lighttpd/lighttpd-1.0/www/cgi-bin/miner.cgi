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
	if [ "`echo "$url" | grep \&`" != "" ] ;then
	    error=true
	    invalid_parameter=$1
	    invalid_value="&"
	    break
	fi
    elif [ "$1" = "account" ] ; then
	account=`urldecode "$2"`
	if [ "`echo "$account" | grep \&`" != "" ] ;then
	    error=true
	    invalid_parameter=$1
	    invalid_value="&"
	    break
	fi
    elif [ "$1" = "password" ] ; then
	password=`urldecode "$2"`
	if [ "`echo "$password" | grep \&`" != "" ] ;then
	    error=true
	    invalid_parameter=$1
	    invalid_value="&"
	    break
	fi
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
    if [ "$invalid_value" = "" ] ; then
	show_msg "Missing mandatory parameter \"$invalid_parameter\""
    else
	show_msg "Invalid value \"$invalid_value\" in parameter \"$invalid_parameter\""
    fi
fi

exit 0
