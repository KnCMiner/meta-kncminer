#!/bin/sh
#set -x

# Read password configuration (if its there)
if [ -s /boot/knc_config/lighttpd-htdigest.user ] ; then
    cp  /boot/knc_config/lighttpd-htdigest.user /etc/lighttpd-htdigest.user
fi
