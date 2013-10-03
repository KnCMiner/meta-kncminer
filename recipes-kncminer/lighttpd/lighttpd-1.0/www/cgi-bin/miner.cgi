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
    elif [ "$1" = "r_mgmt_on" ] ; then
	if [ $2 -eq 1 ] ; then
	    sed -i 's#"api-listen".*:.* false#"api-listen" : true#g' /config/cgminer.conf
	    sed -i 's#"api-network".*:.*false#"api-network" : true#g' /config/cgminer.conf
	else
#	    sed -i 's#"api-listen".*:.*true#"api-listen" : false#g' /config/cgminer.conf	
	    sed -i 's#"api-listen".*:.*true#"api-listen" : true#g' /config/cgminer.conf	
	    sed -i 's#"api-network".*:.*true#"api-network" : false#g' /config/cgminer.conf
	fi
    fi
done

if [ "$error" = "false" ] ; then
    sed -i 's#"url" :.*#"url" : "'${url}'",#g' /config/cgminer.conf
    sed -i 's#"user" :.*#"user" : "'${account}'",#g' /config/cgminer.conf
    sed -i 's#"pass" :.*#"pass" : "'${password}'"#g' /config/cgminer.conf
fi

if [ "$error" = "false" ] ; then
    /etc/init.d/cgminer.sh stop > /dev/null
    /etc/init.d/cgminer.sh start > /dev/null
fi

./get_miner_conf.cgi

exit 0
