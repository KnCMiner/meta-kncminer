FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}-1.0:"

PRINC := "${@int(PRINC) + 1}"

do_install_append() {
	install -m 0755 ${WORKDIR}/mountdevtmpfs.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} mountdevtmpfs.sh start 02 S .

	install -m 0755 ${WORKDIR}/network.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} network.sh start 36 S .

	install -m 0755 ${WORKDIR}/httpdpasswd.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} httpdpasswd.sh start 36 S .

	install -m 0755 ${WORKDIR}/cgminer ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} cgminer start 70 S .
}

SRC_URI_append = " file://mountdevtmpfs.sh"
SRC_URI_append = " file://network.sh"
SRC_URI_append = " file://httpdpasswd.sh"
SRC_URI_append = " file://cgminer"
