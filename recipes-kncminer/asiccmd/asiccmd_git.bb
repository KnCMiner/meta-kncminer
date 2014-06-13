DESCRIPTION = "Hardware initialization routines"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d41d8cd98f00b204e9800998ecf8427e"
PN="asiccmd"

SRCREV = "c4f335dcc07a25142503649fd9ce5712b954cf8c"
PV = "${SRCREV}+git${SRCPV}"

S = "${WORKDIR}/git"

SRC_URI = "git://git@stockholm.kandc.se/projects/kncminer/asic_cmd;protocol=ssh;branch=master"

do_compile_append() {
	make waas
}

do_install() {
        install -d ${D}${bindir}
        install -m 0755 ${S}/io-pwr ${D}${bindir}/io-pwr
        install -m 0755 ${S}/program-fpga ${D}${bindir}/program-fpga
        install -m 0755 ${S}/lcd-message ${D}${bindir}/lcd-message
        install -m 0644 ${S}/spimux.rbf ${D}${bindir}/spimux.rbf
        install -m 0755 ${S}/waas/waas ${D}${bindir}/waas
}
 
inherit pkgconfig
