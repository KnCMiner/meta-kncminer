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

file=/tmp/$$-$RANDOM

trap atexit 0

atexit() {
	rm -rf $file
	umount $file.boot 2>/dev/null || true
	rmdir $file.boot 2>/dev/null || true
	sync
	if [ $pre ]; then
		printf "\n</pre>\n"
		pre=
	fi
	if [ ! $ok ]; then
		printf "<H1>FAILED!</H1>\r\nAn error occurred. See log above<"
	fi
	printf "</body></html>\n"
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
        <link href="../style.css" rel="stylesheet" type="text/css">
        <link href="../grid.css" rel="stylesheet" type="text/css">
        <link href="../type/type.css" rel="stylesheet" type="text/css">
	</head>
	<body>
        <div id="wrapper">
        <header>
        <div id="logo" class="col span_6_of_12">
        <img src="../images/logo.png" alt="KnCMiner logo">
        </div>
        </header>
        <div id="header" class="section">
        <div class="span_12_of_12">
        <div class="xbox box">
        <div class="span_7_of_12">
	<h1>System upgrade</h1>
	<pre>
EOH
pre=1

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
tar zxf -
if [ -f runme.sh ]; then
	sh runme.sh
else
    mkdir $file.boot
    mount /dev/mmcblk0p1 $file.boot
    cp * $file.boot/
    umount $file.boot
    sync
fi

printf "</pre>\r\n"
cat <<EOT
<h1>System upgraded</h1>
<p>The upgrade installed successfully. Please <a href="/cgi-bin/reboot.cgi">reboot</a> to activate.</p>
</div>
</div>
</div>
</div>
</div>
</body>
</html>
EOT

ok=1
