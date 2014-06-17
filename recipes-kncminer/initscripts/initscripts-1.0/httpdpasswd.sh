#!/bin/sh

if [ ! -f /config/lighttpd-htdigest.user ] ; then
    cp /etc/lighttpd-htdigest.user /config/lighttpd-htdigest.user
fi

if [ ! -f /config/shadow ] ; then
    cp -p /etc/shadow.factory /config/shadow
    chmod 0400 /config/shadow
fi
rm -f /etc/shadow
ln -s /config/shadow /etc/shadow
