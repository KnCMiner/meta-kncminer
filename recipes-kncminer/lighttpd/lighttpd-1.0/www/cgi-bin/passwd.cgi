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
	    curr_pw=`echo $2 | sed -f url_escape.sed`
	    hash=`echo -n "admin:KnC Miner configuration:$curr_pw" | md5sum | cut -b -32` 
	    echo "admin:KnC Miner configuration:$hash" > /tmp/validate_pw.tmp.$$
	    diff /config/lighttpd-htdigest.user /tmp/validate_pw.tmp.$$ > /dev/null
	    if [ $? -ne 0 ] ; then
		error=true
		invalid_parameter=$1
		break		
	    fi
	fi
	if [ "$1" = "new_pw" ] ; then
	    new_pw=`echo $2 | sed -f url_escape.sed`
	fi
	if [ "$1" = "new_pw_ctrl" ] ; then
	    new_pw_ctrl=`echo $2 | sed -f url_escape.sed`
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
    show_msg "Missing mandatory parameter \"$invalid_parameter\""
fi
sleep 2

# Apply the new password
if [ "$error" = "false" ] ; then
    # Create new lighttpd-htdigest.user file
    hash=`echo -n "admin:KnC Miner configuration:$new_pw" | md5sum | cut -b -32`
    echo "admin:KnC Miner configuration:$hash" > \
	/config/lighttpd-htdigest.user
fi
