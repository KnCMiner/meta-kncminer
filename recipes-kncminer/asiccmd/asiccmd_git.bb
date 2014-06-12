DESCRIPTION = "Hardware initialization routines"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d41d8cd98f00b204e9800998ecf8427e"
PN="asiccmd"

SRCREV = "752da01fcc1f2f8f3bf672bd78c6076ed895cba6"
PV = "git${SRCREV}"

S = "${WORKDIR}/git"

do_fetch() {
	git clone git@stockholm.kandc.se:projects/kncminer/asic_cmd ${S}
}

do_unpack() {
}

do_configure() {
}

do_install() {
        install -d ${D}${bindir}
        install -m 0755 ${S}/io-pwr ${D}${bindir}/io-pwr
        install -m 0755 ${S}/program-fpga ${D}${bindir}/program-fpga
        install -m 0755 ${S}/lcd-message ${D}${bindir}/lcd-message
        install -m 0644 ${S}/spimux.rbf ${D}${bindir}/spimux.rbf
}
 
inherit pkgconfig
