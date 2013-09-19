#!/bin/sh
. ./cgi_lib.cgi
restart_cgminer=false

if [ -z "$QUERY_STRING" ] ; then
    show_same_page
    exit 0
fi
IFS="&"
set -- $QUERY_STRING

for i in $@; do 
    IFS="="
    set -- $i
    if [ "$1" = "r_mgmt_on" ] && [ $2 -eq 1 ] ; then
	rm /boot/cgminer.conf
	restart_cgminer=true
    fi
done

if [ "$restart_cgminer" = "false" ] ; then
(
    cat <<'EOF'
{
"pools" : [
        {
                "url" : "",
                "user" : "",
                "pass" : ""
        }
]
}
EOF
) > /boot/cgminer.conf
fi

/etc/init.d/miner_config.sh > /dev/null

if [ "$restart_cgminer" = "false" ] ; then
    /etc/init.d/cgminer.sh restart > /dev/null
fi

show_apply_changes

exit 0
