DESCRIPTION = "Cgminer bitcoin miner SW"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

DEPENDS = "ncurses curl"

SRCREV = "7ee5dd785a5dc89d88f9d61e8bf65606ec4b5b70"
PV = "3.3.1+git${SRCPV}"

SRC_URI = "git://git@192.168.1.33/projects/kncminer/cgminer;protocol=ssh;branch=spi-fpga"

S = "${WORKDIR}/git"

EXTRA_OECONF = " \
	     --enable-knc \
	     --disable-adl \
	     --disable-opencl \
	     "
 
inherit autotools pkgconfig
