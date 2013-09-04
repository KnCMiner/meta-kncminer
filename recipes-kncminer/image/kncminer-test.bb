export IMAGE_BASENAME = "kncminer-test"
IMAGE_FSTYPES = "cpio.gz"
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
	kernel-modules \
	dtc \
"

inherit image
