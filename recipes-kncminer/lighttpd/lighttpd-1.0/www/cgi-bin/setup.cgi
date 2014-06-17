#!/bin/sh
. ./cgi_lib.cgi
error=false

IFS="&"
set -- $QUERY_STRING

for i in $@; do 
    IFS="="
    set -- $i
    if [ "$1" = "current_pw" ] ; then
	curr_pw=`urldecode $2`
    fi
    if [ "$1" = "new_pw" ] ; then
	new_pw=`urldecode $2`
    fi
    if [ "$1" = "new_pw_ctrl" ] ; then
	new_pw_ctrl=`urldecode $2`
    fi
    if [ "$1" = "admin" ] ; then
	admin=`urldecode $2`
    fi
    if [ "$1" = "remote_mgmt" ] ; then
	remote_mgmt=`urldecode $2`
    fi
done

if [ "$admin" = "" ]; then
	show_msg "Invalid admin account"
	exit 0
fi
if [ "$new_pw" = "" ] ; then
	show_msg "Invalid password"
	exit 0
fi
if [ "$new_pw_ctrl" != "$new_pw" ] ; then
	show_msg "Password mismatch"
	exit 0
fi

if [ "$remote_mgmt" = "" ]; then
	show_msg "Invalid management network"
	exit 0
fi

hash=`echo -n "${REMOTE_USER}:KnC Miner configuration:$curr_pw" | md5sum | cut -b -32` 
echo "${REMOTE_USER}:KnC Miner configuration:$hash" > /tmp/validate_pw.tmp.$$
diff /config/lighttpd-htdigest.user /tmp/validate_pw.tmp.$$ > /dev/null
if [ $? -ne 0 ] ; then
	show_msg "Wrong password"
	exit 0
fi

# Need to show new page before actually apply'ing new password
show_msg "Saving settings" /

sleep 1

# Apply the new password
# Create new lighttpd-htdigest.user file
hash=`echo -n "${admin}:KnC Miner configuration:$new_pw" | md5sum | cut -b -32`
echo "${admin}:KnC Miner configuration:$hash" > \
    /config/lighttpd-htdigest.user

printf "$new_pw\n$new_pw_ctrl" | passwd root > /dev/null
if [ $? -eq 0 ] ; then
    rm -f /config/shadow
    mv /etc/shadow /config/shadow
    ln -s /config/shadow /etc/shadow
fi

echo "remote_mgmt=\"${remote_mgmt}\"" >>/config/network.conf

if [ ! -f /config/dropbear ]; then
	/etc/init.d/dropbear stop
	echo NO_START=1 >/config/dropbear
fi

QUIET=true /etc/init.d/network.sh
