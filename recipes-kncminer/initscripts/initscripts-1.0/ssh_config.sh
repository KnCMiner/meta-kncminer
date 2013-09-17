#!/bin/sh

# Read password configuration (if its there)
if [ -f /boot/knc_config/dropbear ] ; then
    cp /boot/knc_config/dropbear /etc/default/dropbear
fi
