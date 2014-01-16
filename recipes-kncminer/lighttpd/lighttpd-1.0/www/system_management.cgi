#!/bin/sh
sed -e "
s!#%#REMOTE_USER#%#!${REMOTE_USER}!g
" < /www/tmpl/system_management.html_tmpl
