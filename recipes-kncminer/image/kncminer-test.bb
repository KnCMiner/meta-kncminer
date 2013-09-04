export IMAGE_BASENAME = "kncminer-test"
IMAGE_CLASSES += " image_types_uboot"
IMAGE_TYPES += " cpio.gz.u-boot"
IMAGE_FSTYPES += " cpio.gz.u-boot"
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
