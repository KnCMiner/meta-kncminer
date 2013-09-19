DESCRIPTION = "Daemon to monitor power button"
LICENSE = "GPL"
LIC_FILES_CHKSUM = "file://COPYING;md5=d41d8cd98f00b204e9800998ecf8427e"

SRC_URI = "file://monitor-button.c \
	file://init \
"

S = "${WORKDIR}"

do_compile() {
	make monitor-pwbtn
}

do_install() {
	install -s -m 0755 ${WORKDIR}/monitor-pwbtn ${D}${bindir}
}
