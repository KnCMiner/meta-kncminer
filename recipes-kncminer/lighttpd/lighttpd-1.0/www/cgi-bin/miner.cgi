#!/bin/sh
. ./cgi_lib.cgi
error=false

IFS="&"
set -- $QUERY_STRING

for i in $@; do 
    IFS="="
    set -- $i
    if [ "$2" = "" ] ; then
	# error, all fields are mandatory
	error=true
	invalid_parameter=$1
	break
    elif [ "$1" = "url" ] ; then
	url=$2
    elif [ "$1" = "account" ] ; then
	account=$2
    elif [ "$1" = "password" ] ; then
	password=$2
    fi
done

if [ "$error" = "false" ] ; then
(
    cat <<EOF
{
"pools" : [
        {
                "url" : "$url",
                "user" : "$account",
                "pass" : "$password"
        }
]
}
EOF
) > /boot/cgminer.conf

fi

if [ "$error" = "false" ] ; then
    show_apply_changes
else
    echo "Content-type: text/html"
    echo ""
    
    echo '<html>'
    echo '<head>'
    echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
    echo '<title>NOK</title>'
    echo '</head>'
    echo '<body>'
    echo 'NOK'
    echo 'missing mandatory "'$invalid_parameter'" field'
    
    echo '</body>'
    echo '</html>'
 fi

if [ "$error" = "false" ] ; then
    /etc/init.d/miner_config.sh
    /etc/init.d/cgminer.sh restart > /dev/null
fi

exit 0
