#!/bin/sh -e

# POST upload format:
# -----------------------------29995809218093749221856446032^M
# Content-Disposition: form-data; name="file1"; filename="..."^M
# Content-Type: application/octet-stream^M
# ^M    <--------- headers end with empty line
# file contents
# file contents
# file contents
# ^M    <--------- extra empty line
# -----------------------------29995809218093749221856446032--^M

file=/tmp/$$

trap atexit 0

atexit() {
	rm -rf $file
	umount $file.boot 2>/dev/null || true
	rmdir $file.boot 2>/dev/null || true
	sync
	if [ ! $ok ]; then
	    print "<h1>Restore configuration failed</h1>"
	fi
	printf "</div>"
	printf "</div>"
	printf "</div>"
	printf "</div>"
	printf "</div>"
	printf "</body>"
	printf "</html>"
}

CR=`printf '\r'`

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

IFS="$CR"
read -r delim_line
IFS=""

while read -r line; do
    test x"$line" = x"" && break
    test x"$line" = x"$CR" && break
done

mkdir $file
cd $file
tar xf -
if [ -f restoreConfig.sh ]; then
	sh restoreConfig.sh
else
    exit
fi
rm /config/restoreConfig.sh

cat <<EOT
<h1>System configuration restored</h1>
<p>The backup configuration restored successfully. Please reboot Miner to activate.</p>
<div class="section">                                                         
<div class="col span_6_of_12">
<form action="/cgi-bin/reboot.cgi">
<button type="submit" class="btn btn-lg btn-primary">Reboot</button>
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
