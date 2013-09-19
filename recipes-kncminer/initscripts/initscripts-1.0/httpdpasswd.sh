#!/bin/sh
#set -x

# Read password configuration (if its there)
if [ -s /boot/lighttpd-htdigest.user ] ; then
    cp  /boot/lighttpd-htdigest.user /etc/lighttpd-htdigest.user
fi
