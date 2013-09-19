#!/bin/sh
. ./cgi_lib.cgi

dhcp=false
error=false

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

IFS="&"
set -- $QUERY_STRING

for i in $@; do
    if [ "$i" = "dhcp=on" ] ; then
	dhcp=true
	rm /boot/network.conf
    fi
done

if [ "$dhcp" = false ] ; then
    > /tmp/network.conf.$$
    for i in $@; do 
	IFS="="
	set -- $i
	if [ "$2" = "" ] ; then
	    # error, all fields are mandatory
	    error=true
	    invalid_parameter=$1
	    break
	else
	    valid_ip $2
	    if [ $? -eq 0 ] ; then
		echo $1=$2 >> /tmp/network.conf.$$
	    else
		error=true
		invalid_parameter=$1
		invalid_value=$2
		break
	    fi
	fi
    done
    if [ "$error" = "false" ] ; then
	mv /tmp/network.conf.$$ /boot/network.conf
    else
	rm /tmp/network.conf.$$
    fi
fi

if [ "$error" = "false" ] ; then
    show_apply_changes
else
    echo "Content-type: text/html"
    echo ""
    
    echo '<html>'
    echo '<head>'
    echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
    echo '<title>NOK</title>'
    echo '</head>'
    echo '<body>'
    echo 'NOK'
    if [ "$invalid_value" = "" ] ; then
	echo 'missing mandatory "'$invalid_parameter'" field'
    else
	echo 'invalid value "'$invalid_value'" set for "'$invalid_parameter'" field'
    fi
    echo '</body>'
    echo '</html>'
fi

if [ "$error" = "false" ] ; then
    # "restart" network
    QUIET=true /etc/init.d/network.sh
fi

exit 0
