DESCRIPTION = "Cgminer bitcoin miner SW"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

DEPENDS = "ncurses curl"

SRCREV = "ac3365c70c4458660038522fd015fa0561842b07"
PV = "3.3.1+git${SRCPV}"

SRC_URI = "git://git@192.168.1.33/projects/kncminer/cgminer;protocol=ssh;branch=spi-fpga"

S = "${WORKDIR}/git"

EXTRA_OECONF = " \
	     --enable-knc \
	     --disable-adl \
	     --disable-opencl \
	     "
 
inherit autotools pkgconfig
