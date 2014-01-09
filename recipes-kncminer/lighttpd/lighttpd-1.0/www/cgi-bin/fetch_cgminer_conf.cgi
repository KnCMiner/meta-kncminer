#!/bin/sh
#set -x

BFGMINER_FLAG_FILE="/config/.run_bfgminer"

create_dummy_conf_file()
{
(
cat <<'EOF'
{
"pools" : [
{
"url" : "x",
"user" : "x",
"pass" : "x"
}
]
,
"api-listen" : true
}

EOF
) > /config/cgminer.conf
}

input=`cat /dev/stdin`

if [ "$input" != "null" ] ; then
    if [ "$input" = "FactoryDefault" ] ; then
	if [ -f /config/cgminer.conf.factory ] ; then
	    cp /config/cgminer.conf.factory /config/cgminer.conf
	else
	    create_dummy_conf_file
	fi
	rm -f "$BFGMINER_FLAG_FILE"
    elif [ "$input" = "RestartCGMiner" ] ; then
	/etc/init.d/cgminer.sh restart > /dev/null
    else
#	/usr/bin/validJson "$input" >/dev/null
#	echo a > /dev/null
#	if [ $? -eq 0 ] ; then 
#	    echo "$input" > /config/cgminer.conf
#	fi
	len=${#input}
	if [ $len -gt 0 ] ; then
	    fc=${input:0:1}
	    if [ "$fc" != "{" ] ; then
		if [ "$fc" = "B" ] ; then
		    touch "$BFGMINER_FLAG_FILE"
		else
		    rm -f "$BFGMINER_FLAG_FILE"
		fi
		conf="${input:1}"
	    else
		conf="$input"
	    fi
	    # Perhaps this needs to be re-validated as proper JSON,
	    # even though the web form will not allow to save
	    # if JSON is bad
	    echo "$conf" > /config/cgminer.conf
	fi
    fi
fi

if [ ! -f /config/cgminer.conf ] ; then
    if [ -f /config/cgminer.conf.factory ] ; then
	cp /config/cgminer.conf.factory /config/cgminer.conf
    else
	create_dummy_conf_file
    fi
fi

if [ -f "$BFGMINER_FLAG_FILE" ] ; then
    echo -n B
else
    echo -n C
fi
cat /config/cgminer.conf
