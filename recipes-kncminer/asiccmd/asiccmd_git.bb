DESCRIPTION = "Hardware initialization routines"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=40ed95ac273a015f655b41d0fff4f9b4"
PN="asiccmd"

SRCREV = "v1.0"
PV = "${SRCREV}+git${SRCPV}"

S = "${WORKDIR}/git"

SRC_URI = "git://git@github.com/KnCMiner/knc-asic.git;protocol=ssh;branch=master"

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
