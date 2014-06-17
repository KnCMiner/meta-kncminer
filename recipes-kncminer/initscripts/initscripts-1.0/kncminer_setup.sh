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

ln -sf /config/dropbear /etc/default

# Remove mdns stuff for faster ssh connections
sed -i -e "s/^.*hosts:.*$/hosts:\t\tfiles dns/" /etc/nsswitch.conf

###########################


###########################
# httpdpasswd
if [ ! -f /config/lighttpd-htdigest.user ] ; then
    cp /etc/lighttpd-htdigest.user /config/lighttpd-htdigest.user
fi

# shadow
if [ ! -f /config/shadow ] ; then
    cp -p /etc/shadow.factory /config/shadow
    chmod 0400 /config/shadow
    rm -f /etc/shadow
    ln -s /config/shadow /etc/shadow
else
    rm -f /etc/shadow
    ln -s /config/shadow /etc/shadow
fi
###########################
