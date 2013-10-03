#!/bin/sh

if [ -f /config/cgminer.conf ] ; then
    
    url=`cat /config/cgminer.conf|grep '"url" :' | awk -F\" '{print $4}'`
    account=`cat /config/cgminer.conf|grep '"user" :' | awk -F\" '{print $4}'`
    password=`cat /config/cgminer.conf|grep '"pass" :' | awk -F\" '{print $4}'`
    r_mgmt=`cat /config/cgminer.conf|grep '"api-network" :' | awk '{print $3}'`
    
    if [ "`echo $r_mgmt | grep true`" != "" ] ; then
	sed  '
s&#%#Pool_url#%#&'"$url"'&g
s&#%#Account#%#&'"$account"'&g
s&#%#Password#%#&'"$password"'&g
s&#%#r_mgmt_on_checked#%#&checked&g
s&#%#r_mgmt_off_checked#%#&&g' < /www/tmpl/miner_setting.html_tmpl
    else
	sed  '
s&#%#Pool_url#%#&'"$url"'&g
s&#%#Account#%#&'"$account"'&g
s&#%#Password#%#&'"$password"'&g
s&#%#r_mgmt_on_checked#%#&&g
s&#%#r_mgmt_off_checked#%#&checked&g' < /www/tmpl/miner_setting.html_tmpl
    fi
fi