#!/bin/sh

if [ ! -f /boot/lighttpd-htdigest.user ] ; then
    cp /etc/lighttpd-htdigest.user /boot/lighttpd-htdigest.user
fi
