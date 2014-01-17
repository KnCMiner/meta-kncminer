FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

do_install_append() {
	install -d ${D}/usr/share/snmp/mibs
	install ${WORKDIR}/KNCMINER-MIB.txt ${D}/usr/share/snmp/mibs
}

SRC_URI_append = " file://KNCMINER-MIB.txt \
				"
