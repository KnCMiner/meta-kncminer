#!/bin/sh
sed -e "
s!#%#REMOTE_ADDR#%#!${REMOTE_ADDR}!g
" < /www/tmpl/setup.html_tmpl
