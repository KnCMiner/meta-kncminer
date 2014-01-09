FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}-1.0:"

PRINC := "${@int(PRINC) + 1}"

EXTRA_OECONF += " \
	     --disable-dbus \
	     "
SRC_URI_append = " file://init \
	file://webui.service \
	file://cgminer.service \
	file://avahi-daemon.conf "

do_install_append () {
	install -d ${D}${sysconfdir}/init.d
	install -m 0755 ${WORKDIR}/init ${D}${sysconfdir}/init.d/avahi
	update-rc.d -r ${D} avahi start 50 S .

	install -d ${D}${sysconfdir}/avahi
	install -m 0755 ${WORKDIR}/avahi-daemon.conf ${D}${sysconfdir}/avahi

	install -d ${D}${sysconfdir}/avahi/services
	install -m 0755 ${WORKDIR}/webui.service ${D}${sysconfdir}/avahi/services
	install -m 0755 ${WORKDIR}/cgminer.service ${D}${sysconfdir}/avahi/services
}
