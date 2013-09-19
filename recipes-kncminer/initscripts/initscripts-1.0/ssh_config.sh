#!/bin/sh

# Read password configuration (if its there)
if [ -f /boot/dropbear ] ; then
    cp /boot/dropbear /etc/default/dropbear
fi
