#!/bin/sh
error=false
#set -x

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
	    diff /etc/lighttpd-htdigest.user /tmp/validate_pw.tmp.$$ > /dev/null
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

if [ "$error" = "false" ] ; then
    # Create new lighttpd-htdigest.user
    hash=`echo -n "admin:KnC Miner configuration:$new_pw" | md5sum | cut -b -32`
    echo "admin:KnC Miner configuration:$hash" > \
	/boot/knc_config/lighttpd-htdigest.user
    # Use new passwd file
    /etc/init.d/httpdpasswd.sh
fi


echo "Content-type: text/html"
echo ""
	 
echo '<html>'
echo '<head>'
echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
if [ "$error" = "false" ] ; then
    echo '<title>OK</title>'
    echo '</head>'
    echo '<body>'
    echo 'OK'
else
    echo '<title>NOK</title>'
    echo '</head>'
    echo '<body>'
    echo 'NOK'
    echo 'missing mandatory "'$invalid_parameter'" field'
fi
echo '</body>'
echo '</html>'


# QUERY_STRING='current_pw=sddf&new_pw=&new_pw_ctrl=sdf' /www/pages/cgi-bin/passwd.cgi