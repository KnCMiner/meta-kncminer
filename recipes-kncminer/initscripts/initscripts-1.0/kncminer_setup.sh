#!/bin/sh

###########################
# Release revision
rev=$(cat /etc/knc-release)

if [ -n "$rev" ] ; then
    sed -i "s/irmware.*evision.*/irmware revision: $rev/" /www/pages/firmware_upgrade.html
fi

###########################

###########################
# dropbear
NO_START=0

if [ ! -f /config/dropbear ] ; then
    echo NO_START=1 > /config/dropbear
fi

cp /config/dropbear /etc/default/dropbear

# Remove mdns stuff for faster ssh connections
sed -i -e "s/^.*hosts:.*$/hosts:\t\tfiles/" /etc/nsswitch.conf

###########################


###########################
# miner.conf
# No configuration, create it!
if [ ! -f /config/cgminer.conf ] ; then
    cp /config/cgminer.conf.factory /config/cgminer.conf
fi
###########################


###########################
# httpdpasswd
if [ ! -f /config/lighttpd-htdigest.user ] ; then
    cp /etc/lighttpd-htdigest.user /config/lighttpd-htdigest.user
fi

# shadow
if [ ! -f /config/shadow.factory ] ; then
    cp -p /etc/shadow.factory /config/shadow.factory
    chmod 0400 /config/shadow.factory
fi

if [ ! -f /config/shadow ] ; then
    cp -p /config/shadow.factory /config/shadow
    chmod 0400 /config/shadow
    rm -f /etc/shadow
    ln -s /config/shadow /etc/shadow
else
    rm -f /etc/shadow
    ln -s /config/shadow /etc/shadow
fi
###########################
