#!/bin/sh
case $REMOTE_ADDR in
10.*|192.168.*|172.1[6-9].*|172.2[0-9].*|172.3[01].*)
	adminip=""
	;;
*)
	adminip="$REMOTE_ADDR"
	;;
esac
sed -e "
s!#%#REMOTE_ADDR#%#!${REMOTE_ADDR}!g
s!#%#REMOTE_ADMIN#%#!${adminip}!g
" < /www/tmpl/setup.html_tmpl
