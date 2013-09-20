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
    else
	if [ "$1" = "current_pw" ] ; then 
	    hash=`echo -n "admin:KnC Miner configuration:$2" | md5sum | cut -b -32` 
	    echo "admin:KnC Miner configuration:$hash" > /tmp/validate_pw.tmp.$$
	    diff /boot/lighttpd-htdigest.user /tmp/validate_pw.tmp.$$ > /dev/null
	    if [ $? -ne 0 ] ; then
		error=true
		invalid_parameter=$1
		break		
	    fi
	fi
	if [ "$1" = "new_pw" ] ; then
	    new_pw=$2
	fi
	if [ "$1" = "new_pw_ctrl" ] ; then
	    new_pw_ctrl=$2
	fi
    fi
done

if [ "$new_pw" != "$new_pw_ctrl" ] ; then
    error=true
fi

# Need to show new page before actually apply'ing new password
if [ "$error" = "false" ] ; then
    show_apply_changes
else
    show_error "Missing mandatory parameter \"$invalid_parameter\""
fi
sleep 2

# Apply the new password
if [ "$error" = "false" ] ; then
    # Create new lighttpd-htdigest.user file
    hash=`echo -n "admin:KnC Miner configuration:$new_pw" | md5sum | cut -b -32`
    echo "admin:KnC Miner configuration:$hash" > \
	/boot/lighttpd-htdigest.user
fi
