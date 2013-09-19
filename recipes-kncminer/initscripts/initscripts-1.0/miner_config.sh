#!/bin/sh

# No configuration, create it!
if [ ! -f /boot/cgminer.conf ] ; then
(
    cat <<'EOF'
{
"pools" : [
        {
                "url" : "http://192.168.1.45:3334",
                "user" : "a",
                "pass" : "a"
        }
]
,
"api-listen" : true
}
EOF
) > /boot/cgminer.conf
fi

# check if remote management
if [ "`cat /boot/cgminer.conf|grep api-listen.*true`" != "" ] ; then
    # remote management, setup  stunnel if its down
    echo setting up stunnel if its down

    # fix web presentation
    # check box for remote service check box
    # invalid textfields for manual setup

else
    # no remote management, take down stunnel if its up
    echo teardown stunnel if its up

    # fix web presentation
    url=`cat /boot/cgminer.conf|grep '"url" :' | awk -F\" '{print $4}'`
    account=`cat /boot/cgminer.conf|grep '"user" :' | awk -F\" '{print $4}'`
    password=`cat /boot/cgminer.conf|grep '"pass" :' | awk -F\" '{print $4}'`

    sed  '
s/@%@Pool_url@%@/'$url'/g
s/@%@Account@%@/'$account'/g
s/@%@Password@%@/'$password'/g' < /www/tmpl/miner_setting.html_tmpl > /www/pages/miner_setting.html
    
    #uncheck box for remote service check box
fi
