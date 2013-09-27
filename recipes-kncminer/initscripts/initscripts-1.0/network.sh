#!/bin/sh

if [ ! -f /config/network.conf ] ; then
    cp /config/network.conf.factory /config/network.conf
fi

# Read network configuration
if [ -s /config/network.conf ] ; then
    . /config/network.conf
fi

if [ -n "$hostname" ] ; then
	hostname $hostname
	echo $hostname > /etc/hostname
fi

# Setup link 
ip link set lo up
ip link set eth0 up

ip addr flush dev eth0

if [ "$dhcp" = "true" ] ; then
    if [ "$QUIET" = "true" ] ; then
        udhcpc -b -x hostname:$hostname eth0 > /dev/null
    else
        udhcpc -b -x hostname:$hostname eth0
    fi

    # "create" webpage from template
    sed '
s/#%#checked#%#/checked/g
s/#%#IP_Address#%#//g
s/#%#Netmask#%#//g
s/#%#Gateway#%#//g
s/#%#DNSServers#%#//g' < /www/tmpl/network_setting.html_tmpl > /www/pages/network_setting.html
else
    # Manual setup
    ip addr add $ipaddress/$netmask dev eth0
    
    ip ro add default via $gateway

    > /etc/resolv.conf
    for ip in $dnsservers ; do
	echo nameserver $ip >> /etc/resolv.conf
    done

    # "create" webpage from template
    sed  '
s/#%#checked#%#//g
s/#%#IP_Address#%#/'$ipaddress'/g
s/#%#Netmask#%#/'$netmask'/g
s/#%#Gateway#%#/'$gateway'/g
s/#%#DNSServers#%#/'"$dnsservers"'/g' < /www/tmpl/network_setting.html_tmpl > /www/pages/network_setting.html

fi
