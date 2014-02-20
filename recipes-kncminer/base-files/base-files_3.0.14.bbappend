FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}-1.0:"

PRINC := "${@int(PRINC) + 1}"

do_install_append() {
	install -m 0644 ${WORKDIR}/fstab ${D}${sysconfdir}
	install -m 0644 ${WORKDIR}/knc-release ${D}${sysconfdir}
	install -d ${D}/config
}

SRC_URI_append = " file://fstab \
		   file://knc-release"
