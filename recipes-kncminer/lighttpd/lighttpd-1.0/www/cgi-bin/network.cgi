#!/bin/sh
. ./cgi_lib.cgi

dhcp=false
error=false
dnsservers=""

valid_ip()
{
    local  ip=$1
    local  stat=0

    if [ "`echo $ip | grep -E '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'`" = "$ip" ]; then
        OIFS=$IFS
        IFS='.'
	
	for octet in $ip ; do
	    if [ ! $octet -le 255 ] ; then
		stat=1
	    fi
	done
        IFS=$OIFS
    else
	stat=1
    fi
    return $stat
}

valid_hostname()
{
    local  hostname="$1"
    local  stat=1

    if [ -n "$hostname" ] && [ "`echo $hostname | grep -E '^[0-9a-zA-Z-]{1,63}$'`" = "$hostname" ]; then
	stat=0;
    fi
    return $stat
}

if [ -f /etc/hostname ] ; then
    current_hostname=`cat /etc/hostname`
else
    current_hostname=Jupiter-XXX
fi

IFS="&"
set -- $QUERY_STRING

> /tmp/network.conf.$$
for i in $@; do
    IFS="="
    set -- $i
    if [ "$1" = "dhcp" ] ; then
	echo $1=$2 >> /tmp/network.conf.$$
	dhcp=true
    elif [ "$1" = "hostname" ] ; then
	if [ "$2" != "" ] ; then
	    input_hostname=`urldecode $2`
	    if [ "`echo "$input_hostname" | grep '\\\'`" != "" ] ; then
		input_hostname=`echo "$input_hostname" | sed 's!\\\!\\\\\\\!g'`
	    fi
	    if [ "`echo "$input_hostname" | grep \&`" != "" ] ;then
		input_hostname=`echo "$input_hostname" | sed 's!\&!\\\&!g'`
	    fi
	    valid_hostname "$input_hostname"
	    if [ $? -eq 0 ] ; then
		echo $1="$input_hostname" >> /tmp/network.conf.$$
	    else
		echo "hostname=$current_hostname" >> /tmp/network.conf.$$
	    fi
	else
	    echo "hostname=$current_hostname" >> /tmp/network.conf.$$
	fi
    elif [ "$1" = "ntpserver" ]; then
	echo "ntpserver=\"`urldecode "$2"`\"" >> /tmp/network.conf.$$
    elif [ "$1" = "remote_mgmt" ]; then
	echo "remote_mgmt=\"`urldecode "$2"`\"" >> /tmp/network.conf.$$
    elif [ "$1" = "snmp_managers" ]; then
	echo "SNMP_MANAGERS=\"`urldecode "$2"`\"" >> /tmp/network.conf.$$
    elif [ "$1" = "snmp_community" ]; then
	echo "SNMP_COMMUNITY=\"`urldecode "$2"`\"" >> /tmp/network.conf.$$
    fi
done

IFS="&"
set -- $QUERY_STRING

if [ "$dhcp" != true ] ; then
    for i in $@; do 
	IFS="="
	set -- $i
	if [ "$1" = "dnsservers" ] ; then
	    dnsservers="`urldecode "$2"`"
	elif [ "$1" = "dhcp" ]; then
	    : # handled above
	elif [ "$1" = "hostname" ]; then
	    : # handled above
	elif [ "$1" = "ntpserver" ]; then
	    : # handled above
	elif [ "$1" = "remote_mgmt" ]; then
	    : # handled above
	elif [ "$1" = "old-remote_mgmt" ]; then
	    : # GUI artefact, not saved
	elif [ "$1" = "snmp_managers" ]; then
	    : # handled above
	elif [ "$1" = "snmp_community" ]; then
	    : # handled above
	elif [ "$2" = "" ] ; then
	    # error, all fields are mandatory
	    error=true
	    invalid_parameter=$1
	    break
	else
	    v="`urldecode $2`"
	    valid_ip $v
	    if [ $? -eq 0 ] ; then
		echo $1=$v >> /tmp/network.conf.$$

		if [ "$1" = "gateway" ] ; then
		    gateway=$v
		fi
	    else
		error=true
		invalid_parameter=$1
		invalid_value=$v
		break
	    fi
	fi
    done

    if [ "$dnsservers" = "" ] ; then
	echo "dnsservers=\""$gateway\" >> /tmp/network.conf.$$
    else
	echo "dnsservers=\""$dnsservers\" >> /tmp/network.conf.$$
    fi
fi

if [ "$error" = "false" ] ; then
    show_msg "Saving settings"
    mv /tmp/network.conf.$$ /config/network.conf
    QUIET=true /etc/init.d/network.sh
    if [ "$current_hostname" != "$input_hostname" ] ; then
	/etc/init.d/avahi restart > /dev/null
    fi
else
    show_msg "Error $invalid_parameter=$invalid_value"
    rm /tmp/network.conf.$$
    sleep 5
fi

exit 0
