#!/bin/sh
#set -x

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
"api-listen" : true,
"api-network" : true,
"api-allow" : "W:0/0"
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
    elif [ "$input" = "RestartCGMiner" ] ; then
	/etc/init.d/cgminer.sh stop > /dev/null
        /etc/init.d/cgminer.sh start > /dev/null
    else
#	/usr/bin/validJson "$input" >/dev/null
#	echo a > /dev/null
#	if [ $? -eq 0 ] ; then 
#	    echo "$input" > /config/cgminer.conf
#	fi
	# Perhaps this nees to be re validated as proper JSON,
	# even though the web form will nor allow to save
	# if JSON is bad
	echo "$input" > /config/cgminer.conf
    fi
fi

if [ ! -f /config/cgminer.conf ] ; then
    if [ -f /config/cgminer.conf.factory ] ; then
	cp /config/cgminer.conf.factory /config/cgminer.conf
    else
	create_dummy_conf_file
    fi
fi

cat /config/cgminer.conf

