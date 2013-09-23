#!/bin/sh
NO_START=0

if [ ! -f /config/dropbear ] ; then
    echo NO_START=1 > /config/dropbear
fi
cp /config/dropbear /etc/default/dropbear
. /etc/default/dropbear

if [ $NO_START -eq 1 ] ; then
    sed '
s/#%#ssh_on_checked#%#//g
s/#%#ssh_off_checked#%#/checked/g' < /www/tmpl/services_conf.html_tmpl > /www/pages/services_conf.html
else
    sed '
s/#%#ssh_on_checked#%#/checked/g
s/#%#ssh_off_checked#%#//g' < /www/tmpl/services_conf.html_tmpl > /www/pages/services_conf.html
fi
