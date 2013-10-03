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

if [ -f /etc/hostname ] ; then
    hn=`cat /etc/hostname`
else
    hn=Jupiter-XXX
fi

IFS="&"
set -- $QUERY_STRING

for i in $@; do
    if [ "$i" = "dhcp=on" ] ; then
	echo dhcp=true > /config/network.conf
	echo "hostname=$hn" >> /config/network.conf
	dhcp=true
    fi
done

if [ "$dhcp" = false ] ; then
    > /tmp/network.conf.$$
    echo "hostname=$hn" >> /tmp/network.conf.$$
    for i in $@; do 
	IFS="="
	set -- $i
	if [ "$1" = "dnsservers" ] ; then
	    IFS="+"
	    set -- $2
	    for j in $@; do
		if [ "$j" != "" ] ; then
		    valid_ip $j
		    if [ $? -eq 0 ] ; then
			if [ "$dnsservers" = "" ] ; then
			    dnsservers=${j}
			else
			    dnsservers="${j} ${dnsservers}"
			fi
		    fi
		fi
	    done
	    IFS="="
	elif [ "$2" = "" ] ; then
	    # error, all fields are mandatory
	    error=true
	    invalid_parameter=$1
	    break
	else
	    valid_ip $2
	    if [ $? -eq 0 ] ; then
		echo $1=$2 >> /tmp/network.conf.$$

		if [ "$1" = "gateway" ] ; then
		    gateway=$2
		fi
	    else
		error=true
		invalid_parameter=$1
		invalid_value=$2
		break
	    fi
	fi
    done

    if [ "$dnsservers" = "" ] ; then
	echo "dnsservers=\""$gateway\" >> /tmp/network.conf.$$
    else
	echo "dnsservers=\""$dnsservers\" >> /tmp/network.conf.$$
    fi

    if [ "$error" = "false" ] ; then
	mv /tmp/network.conf.$$ /config/network.conf
    else
	rm /tmp/network.conf.$$
    fi
fi

if [ "$error" = "false" ] ; then
    QUIET=true /etc/init.d/network.sh
    show_apply_changes
else
    if [ "$invalid_value" = "" ] ; then
	show_msg "Missing mandatory parameter \"$invalid_parameter\""
    else
	show_msg "Invalid value \"$invalid_value\" in parameter \"$invalid_parameter\""
    fi
fi

exit 0
