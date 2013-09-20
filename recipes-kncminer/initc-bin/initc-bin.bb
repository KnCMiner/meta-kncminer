DESCRIPTION = "Initc application for production images for Kncminers"
LICENSE = "unknown"
LIC_FILES_CHKSUM = "file://COPYING;md5=d41d8cd98f00b204e9800998ecf8427e"

SRC_URI = "file://initc \
	file://spitop_bitrev_pad.rbf \
	file://initc.sh \
	file://COPYING"

S = "${WORKDIR}"

do_install() {
        install -d ${D}${bindir}
        install -m 0755 ${S}/initc ${D}${bindir}
        install -m 0644 ${S}/spitop_bitrev_pad.rbf ${D}${bindir}

        install -d ${D}${sysconfdir}/init.d
	install -m 0755 ${WORKDIR}/initc.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} initc.sh start 36 S .
}
