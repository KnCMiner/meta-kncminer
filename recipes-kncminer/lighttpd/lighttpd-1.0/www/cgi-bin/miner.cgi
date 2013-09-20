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
	url=$2
    elif [ "$1" = "account" ] ; then
	account=$2
    elif [ "$1" = "password" ] ; then
	password=$2
    fi
done

if [ "$error" = "false" ] ; then
    sed -i '
s/"url" :.*/"url" : "'$url'"/g
s/"user" :.*/"user" : "'$account'"/g
s/"pass" :.*/"pass" : "'$password'"/g' /boot/cgminer.conf
fi

if [ "$error" = "false" ] ; then
    show_apply_changes
else
    show_error "Missing mandatory parameter \"$invalid_parameter\""
fi

if [ "$error" = "false" ] ; then
    /etc/init.d/miner_config.sh
    /etc/init.d/cgminer.sh restart > /dev/null
fi

exit 0
