#!/bin/sh -e

file=backupKNC_`date +%Y-%m-%d_%H%M%S`.tar
dir=/tmp/backup$$
bkup_files="advanced.conf \
    dropbear \
    dropbear_rsa_host_key \
    led-blink.conf \
    lighttpd-htdigest.user \
    network.conf \
    shadow \
    shadow.factory \
    cgminer.conf \
    cgminer.conf.factory"


trap atexit 0

atexit() {
	rm -rf $dir

	sync
	if [ ! $ok ]; then
	    print "<h1>Create backup failed</h1>"
	fi
	printf "</div>"
	printf "</div>"
	printf "</div>"
	printf "</div>"
	printf "</div>"
	printf "</body>"
	printf "</html>"
}

# CGI output must start with at least empty line (or headers)
printf "Content-type: text/html\r\n\r\n"

cat <<-EOH
        <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">
	<html>
	<head>
	<title>Miner</title>
        <meta charset="UTF-8" />
        <link href="/style.css" rel="stylesheet" type="text/css">
        <link href="/grid.css" rel="stylesheet" type="text/css">
        <link href="/type/type.css" rel="stylesheet" type="text/css">
	</head>
	<body>
        <div id="wrapper">
        <header>
        <div id="logo" class="col span_6_of_12">
        <img src="/images/logo.png" alt="KnCMiner logo">
        </div>
        </header>
        <div id="header" class="section">
        <div class="span_12_of_12">
        <div class="xbox box">
        <div class="span_12_of_12">
EOH

exec 2>&1

mkdir $dir
cd $dir

for f in $bkup_files ; do
    if [ -f /config/$f ] ; then  
	cp /config/$f .
    fi
done

> ./restoreConfig.sh
echo 'DATE=`date +%Y-%m-%d_%H%M%S`'                      >> ./restoreConfig.sh
echo 'mkdir -p /config/.old_config'                      >> ./restoreConfig.sh
echo 'mkdir /config/.old_config/config_$DATE'            >> ./restoreConfig.sh
echo 'mv /config/* /config/.old_config/config_$DATE/'    >> ./restoreConfig.sh
echo 'cp * /config'                                      >> ./restoreConfig.sh
echo 'NOOF_DIR=0 '                                       >> ./restoreConfig.sh
echo 'for dir in `ls -t /config/.old_config` ; do'       >> ./restoreConfig.sh
echo '    if [ -d /config/.old_config/$dir ] ; then'     >> ./restoreConfig.sh
echo '        NOOF_DIR=`expr $NOOF_DIR + 1`'             >> ./restoreConfig.sh
echo '        if [ $NOOF_DIR -gt 3 ] ; then'             >> ./restoreConfig.sh
echo '            rm -rf /config/.old_config/$dir'       >> ./restoreConfig.sh
echo '        fi'                                        >> ./restoreConfig.sh
echo '    fi'                                            >> ./restoreConfig.sh
echo 'done'                                              >> ./restoreConfig.sh
echo 'sync'                                              >> ./restoreConfig.sh

tar cf /www/pages/$file *
if [ $? -ne 0 ] ; then
    exit
fi

cat <<EOT
<h1>Backup created</h1>
<p>Save backup to PC.</p>
<div class="section">                                                         
<div class="col span_6_of_12">
<form action="/$file">
<button type="submit" class="btn btn-lg btn-primary">Save</button>
</form>
</div>
<div class="col span_6_of_12">                                        
<form action="/firmware_upgrade.html">                                                         
<button style="float: right" type="submit" class="btn btn-lg btn-secondary">Go Back</button>
</form>                                                                        
</div>
</div>
<div class="section"></div>
</div>
</div>
</div>
</div>
</body>
</html>
EOT

ok=1
