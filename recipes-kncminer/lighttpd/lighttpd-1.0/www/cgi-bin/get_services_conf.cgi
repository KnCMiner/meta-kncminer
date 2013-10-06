#!/bin/sh

if [ -f /etc/default/dropbear ] ; then
    . /etc/default/dropbear
fi

if [ $NO_START -eq 1 ] ; then
    sed '
s/#%#ssh_on_checked#%#//g
s/#%#ssh_off_checked#%#/checked/g' < /www/tmpl/services_conf.html_tmpl
else
    sed '
s/#%#ssh_on_checked#%#/checked/g
s/#%#ssh_off_checked#%#//g' < /www/tmpl/services_conf.html_tmpl
fi
