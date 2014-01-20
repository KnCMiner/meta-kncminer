FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

do_install_append() {
	install -d ${D}/usr/share/snmp/mibs
	install ${WORKDIR}/KNCMINER-MIB.txt ${D}/usr/share/snmp/mibs

	install -d ${D}${sysconfdir}/snmp/
	install ${WORKDIR}/snmp.conf ${D}${sysconfdir}/snmp

	install -d ${D}${sysconfdir}/init.d/
	install -m 0755 ${WORKDIR}/loop.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} loop.sh start 80 S .
}

FILES_${PN}-client += "${sysconfdir}/init.d ${sysconfdir}/rcS.d ${sysconfdir}/snmp"

SRC_URI_append = " file://KNCMINER-MIB.txt"
SRC_URI_append = " file://snmp.conf"
SRC_URI_append = " file://loop.sh"
