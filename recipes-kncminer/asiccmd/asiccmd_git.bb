DESCRIPTION = "Hardware initialization routines"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d41d8cd98f00b204e9800998ecf8427e"
PN="asiccmd"

SRCREV = "cda6346b2717cd6479b742308a92aeff3be8ac38"
PV = "${SRCREV}+git${SRCPV}"

S = "${WORKDIR}/git"

SRC_URI = "git://git@stockholm.kandc.se/projects/kncminer/asic_cmd;protocol=ssh;branch=master"

do_compile_append() {
	make waas
}

do_install() {
        install -d ${D}${bindir}
        install -m 0755 ${S}/asic ${D}${bindir}/asic
        install -m 0755 ${S}/io-pwr ${D}${bindir}/io-pwr
        install -m 0755 ${S}/program-fpga ${D}${bindir}/program-fpga
        install -m 0755 ${S}/lcd-message ${D}${bindir}/lcd-message
        install -m 0755 ${S}/knc-serial ${D}${bindir}/knc-serial
        install -m 0644 ${S}/spimux.rbf ${D}${bindir}/spimux.rbf
        install -m 0755 ${S}/waas/waas ${D}${bindir}/waas
}
 
inherit pkgconfig
