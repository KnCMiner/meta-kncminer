#!/bin/sh
NO_START=0

if [ ! -f /config/dropbear ] ; then
    echo NO_START=1 > /config/dropbear
fi

