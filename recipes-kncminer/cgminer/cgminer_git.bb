DESCRIPTION = "Cgminer bitcoin miner SW"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

DEPENDS = "ncurses curl"

SRCREV = "v4.4.0-knc2.0"
PV = "${SRCREV}+git${SRCPV}"

SRC_URI = "git://git@github.com:KnCMiner/knc-asic.git;protocol=ssh;branch=knc2"

S = "${WORKDIR}/git"

CFLAGS_prepend = "-I ${S}/compat/jansson-2.5/src"

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
