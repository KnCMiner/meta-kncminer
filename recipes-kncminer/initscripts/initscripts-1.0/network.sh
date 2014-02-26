#!/bin/sh

if [ ! -f /config/network.conf ] ; then
    cp /config/network.conf.factory /config/network.conf
fi

# Read network configuration
if [ -s /config/network.conf ] ; then
    . /config/network.conf
else
    dhcp=true
    hostname=Jupiter-XXX
fi

# Setup ntp server
if [ "x$ntpserver" != "x" ] ; then
  sed -i "s/^server pool.ntp.org.*$/server $ntpserver/" /etc/ntp.conf
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
else
    # Manual setup
    ip addr add $ipaddress/$netmask dev eth0
    
    ip ro add default via $gateway

    > /etc/resolv.conf
    for ip in $dnsservers ; do
	echo nameserver $ip >> /etc/resolv.conf
    done

    /etc/firewall_setup
fi
