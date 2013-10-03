#!/bin/sh

# Change this to produce "static text" on the status page, like HW revision and such"
killall -0 cgminer
if [ $? = 0 ] ; then
    sed '
s!#%#Color#%#!green!g
s!#%#Status#%#!Running!g' < /www/tmpl/index.html_tmpl

else
    sed '
s!#%#Color#%#!red!g
s!#%#Status#%#!Stopped!g' < /www/tmpl/index.html_tmpl

fi


