export IMAGE_BASENAME = "kncminer"
IMAGE_INSTALL = " \
	busybox \
	base-files \
	base-passwd \
	initscripts \
	sysvinit \
	sysvinit-pidof \
	angstrom-version \
	tinylogin \
	i2c-tools \
	screen \
	dropbear \
	libcurl \
	lighttpd \
	cgminer \
	bfgminer \
	dtc \
	stunnel \
	initc-bin \
	openssl \
	curl \
	monitor-pwbtn \
	ntp \
	ntpdate \
	netbase \
	avahi \
	led-blink \
	iptables \
"

inherit image
