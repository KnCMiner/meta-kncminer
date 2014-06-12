DESCRIPTION = "Simple tool for testing SPI transfers"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263"

SRCREV = "16eadee04193a565086090c726c025c4f8f4ca57"
PV = "${SRCREV}+git${SRCPV}"

SRC_URI = "git://github.com/KnCMiner/spi-test.git;protocol=https;branch=master"

S = "${WORKDIR}/git"

do_compile() {
	make spi-test-simple
}

do_install() {
        install -d ${D}${bindir}
        install -m 0755 ${S}/spi-test ${D}${bindir}/spi-test
}
 
inherit pkgconfig
