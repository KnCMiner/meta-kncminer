#!/bin/sh

# Read network configuration
if [ -s /config/network.conf ] ; then
    . /config/network.conf
fi

# "create" webpage from template
if [ "$dhcp" = "true" ] ; then
    sed '
s/#%#checked#%#/checked/g
s/#%#Hostname#%#/'$hostname'/g
s/#%#IP_Address#%#//g
s/#%#Netmask#%#//g
s/#%#Gateway#%#//g
s/#%#DNSServers#%#//g' < /www/tmpl/network_setting.html_tmpl
else
    sed  '
s/#%#checked#%#//g
s/#%#Hostname#%#/'$hostname'/g
s/#%#IP_Address#%#/'$ipaddress'/g
s/#%#Netmask#%#/'$netmask'/g
s/#%#Gateway#%#/'$gateway'/g
s/#%#DNSServers#%#/'"$dnsservers"'/g' < /www/tmpl/network_setting.html_tmpl

fi
