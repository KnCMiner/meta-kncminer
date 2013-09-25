#!/bin/sh

dd if=/sys/bus/i2c/devices/1-0054/eeprom  bs=32 count=1  of=/tmp/eeprom.$$ > /dev/null

# Find the serial number
if [ -f /tmp/eeprom.$$ ] ; then
    serial=$(cat /tmp/eeprom.$$)
    rm /tmp/eeprom.$$
else
    serial=Unknown
fi

if [ ! -f /config/network.conf ] ; then
    cp /config/network.conf.factory /config/network.conf
fi

# Read network configuration
if [ -s /config/network.conf ] ; then
    . /config/network.conf
fi

# Setup link 
ip link set lo up
ip link set eth0 up

ip addr flush dev eth0

if [ "$dhcp" = "true" ] ; then
    if [ "$QUIET" = "true" ] ; then
        udhcpc -b -x hostname:$serial eth0 > /dev/null
    else
        udhcpc -b -x hostname:$serial eth0
    fi

    # "create" webpage from template
    sed '
s/#%#checked#%#/checked/g
s/#%#IP_Address#%#/IP Address/g
s/#%#Netmask#%#/Netmask/g
s/#%#Gateway#%#/Gateway/g
s/#%#DNSServers#%#/DNS Servers/g' < /www/tmpl/network_setting.html_tmpl > /www/pages/network_setting.html
else
    # Manual setup
    ip addr add $ipaddress/$netmask dev eth0
    
    ip ro add default via $gateway

    dns=`echo $dnsservers|sed 's/,/ /g'`
    > /etc/resolv.conf
    for ip in $dns ; do
	echo nameserver $ip >> /etc/resolv.conf
    done

    # "create" webpage from template
    sed  '
s/#%#checked#%#//g
s/#%#IP_Address#%#/'$ipaddress'/g
s/#%#Netmask#%#/'$netmask'/g
s/#%#Gateway#%#/'$gateway'/g
s/#%#DNSServers#%#/'"$dns"'/g' < /www/tmpl/network_setting.html_tmpl > /www/pages/network_setting.html


fi
