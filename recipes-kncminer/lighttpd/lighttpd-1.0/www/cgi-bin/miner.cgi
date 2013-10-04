#!/bin/sh
. ./cgi_lib.cgi
error=false

OIFS=$IFS
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
        if [ "`echo "$url" | grep '\\\'`" != "" ] ; then
            url=`echo "$url" | sed 's!\\\!\\\\\\\!g'`
        fi
	if [ "`echo "$url" | grep \&`" != "" ] ;then
            url=`echo "$url" | sed 's!\&!\\\&!g'`
	fi
    elif [ "$1" = "account" ] ; then
	account=`urldecode "$2"`
        if [ "`echo "$account" | grep '\\\'`" != "" ] ; then
            account=`echo "$account" | sed 's!\\\!\\\\\\\!g'`
        fi
	if [ "`echo "$account" | grep \&`" != "" ] ;then
            account=`echo "$account" | sed 's!\&!\\\&!g'`
	fi
    elif [ "$1" = "password" ] ; then
	password=`urldecode "$2"`
        if [ "`echo "$password" | grep '\\\'`" != "" ] ; then
            password=`echo "$password" | sed 's!\\\!\\\\\\\!g'`
        fi
	if [ "`echo "$password" | grep \&`" != "" ] ; then
            password=`echo "$password" | sed 's!\&!\\\&!g'`
	fi
    elif [ "$1" = "r_mgmt_on" ] ; then
	if [ $2 -eq 1 ] ; then
	    remote_mgmt=true
	else
	    remote_mgmt=false
	fi
    fi
done
IFS=$OIFS

if [ "$error" = "false" ] ; then
    (
	cat <<'EOF'
{
"pools" : [
{
"url" : "a",
"user" : "b",
"pass" : "c"
}
]
,
"api-listen" : true,
"api-network" : true,
"api-allow" : "W:0/0"
}

EOF
    ) > /config/cgminer.conf

    sed -i 's"\"url\" :.*"\"url\" : \"'${url}'\","g' /config/cgminer.conf
    sed -i 's"\"user\" :.*"\"user\" : \"'${account}'\","g' /config/cgminer.conf
    sed -i 's"\"pass\" :.*"\"pass\" : \"'${password}'\""g' /config/cgminer.conf
    if [ $remote_mgmt = true ] ; then 
	sed -i 's#"api-listen".*:.* false#"api-listen" : true#g' /config/cgminer.conf
	sed -i 's#"api-network".*:.*false#"api-network" : true#g' /config/cgminer.conf
    else
	sed -i 's#"api-listen".*:.*true#"api-listen" : false#g' /config/cgminer.conf	
	sed -i 's#"api-network".*:.*true#"api-network" : false#g' /config/cgminer.conf
    fi
fi

if [ "$error" = "false" ] ; then
    /etc/init.d/miner_config.sh
    /etc/init.d/cgminer.sh stop > /dev/null
    /etc/init.d/cgminer.sh start > /dev/null
    show_apply_changes
else
    if [ "$invalid_value" = "" ] ; then
	show_msg "Missing mandatory parameter \"$invalid_parameter\""
    else
	show_msg "Invalid value \"$invalid_value\" in parameter \"$invalid_parameter\""
    fi
fi

exit 0
