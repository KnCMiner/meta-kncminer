#!/bin/sh

if [ ! -f /boot/dropbear ] ; then
    echo NO_START=1 > /boot/dropbear
fi
cp /boot/dropbear /etc/default/dropbear
