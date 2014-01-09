#!/bin/sh

# Read network configuration
if [ -s /config/network.conf ] ; then
    . /config/network.conf
fi

# "create" webpage from template
if [ "$dhcp" = "true" ] ; then
    dhcp=checked
    ipaddress=""
    netmask=""
    gateway=""
    dnsservers=""
else
    dhcp=""
fi

sed  "
s!#%#dhcp#%#!$dhcp!g
s!#%#remote_mgmt#%#!$remote_mgmt!g
s!#%#Hostname#%#!$hostname!g
s!#%#IP_Address#%#!$ipaddress!g
s!#%#Netmask#%#!$netmask!g
s!#%#Gateway#%#!$gateway!g
s!#%#DNSServers#%#!$dnsservers!g
s!#%#REMOTE_ADDR#%#!$REMOTE_ADDR!g
" < /www/tmpl/network_setting.html_tmpl
