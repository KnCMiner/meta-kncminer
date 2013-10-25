DESCRIPTION = "Cgminer bitcoin miner SW"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

DEPENDS = "ncurses curl"

SRCREV = "v3.4.0-knc-0.96.1"
PV = "${SRCREV}"

SRC_URI = "git://github.com/KnCMiner/cgminer.git;protocol=https;branch=knc-spi-fpga"

S = "${WORKDIR}/git"

CFLAGS_prepend = "-I ${S}/compat/jansson "

EXTRA_OECONF = " \
	     --enable-knc \
	     --disable-adl \
	     --disable-opencl \
	     "

do_compile_append() {
	make api-example
}

do_install_append() {
        install -d ${D}${bindir}
        install -m 0755 ${S}/api-example ${D}${bindir}/api-cgminer
}
 
inherit autotools pkgconfig
