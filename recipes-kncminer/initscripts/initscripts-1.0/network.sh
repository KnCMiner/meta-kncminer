#!/bin/sh

dd if=/sys/bus/i2c/devices/2-0054/eeprom  bs=32 count=1  of=/tmp/eeprom.$$ > /dev/null

if [ -f /tmp/eeprom.$$ ] ; then
    if [ -s /tmp/eeprom.$$ ] ; then
	> /tmp/prod_data.conf.$$
	
	while read line ; do
	    echo $line >> /tmp/prod_data.conf.$$
	done < /tmp/eeprom.$$
    fi
    rm /tmp/eeprom.$$
fi

# Find the serial number
if [ -f /tmp/prod_data.conf.$$ ] ; then
    . /tmp/prod_data.conf.$$
    rm /tmp/prod_data.conf.$$
else
    serial=9999
fi

# Read network configuration (if its there)
if [ -s /boot/knc_config/network.conf ] ; then
    . /boot/knc_config/network.conf
fi

# Setup link 
ip link set lo up
ip link set eth0 up

ip addr flush dev eth0

if [ "$ipaddress" != "" ] && [ "$netmask" != "" ] && 
    [ "$gateway" != "" ] ; then
    # Manual setup
    ip addr add $ipaddress/$netmask dev eth0
    
    ip ro add default via $gateway
    echo nameserver $gateway >/etc/resolv.conf

    # "create" webpage from template
    sed  '
s/@%@checked@%@//g
s/@%@IP_Address@%@/'$ipaddress'/g
s/@%@Netmask@%@/'$netmask'/g
s/@%@Gateway@%@/'$gateway'/g' < /www/tmpl/network_setting.html_tmpl > /www/pages/network_setting.html

else
    if [ "$QUIET" = "true" ] ; then
        udhcpc -v -x hostname:$serial eth0 > /dev/null
    else
        udhcpc -v -x hostname:$serial eth0
    fi

    # "create" webpage from template
    sed '
s/@%@checked@%@/checked/g
s/@%@IP_Address@%@/IP Address/g
s/@%@Netmask@%@/Netmask/g
s/@%@Gateway@%@/Gateway/g' < /www/tmpl/network_setting.html_tmpl > /www/pages/network_setting.html

fi
