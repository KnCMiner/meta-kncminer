FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

do_install_append() {
	install -d ${D}/usr/share/snmp/mibs
	install ${WORKDIR}/KNCMINER-MIB.txt ${D}/usr/share/snmp/mibs

	install -d ${D}/etc/snmp/
	install ${WORKDIR}/snmp.conf ${D}/etc/snmp
}

SRC_URI_append = " file://KNCMINER-MIB.txt \
		file://snmp.conf \
				"
