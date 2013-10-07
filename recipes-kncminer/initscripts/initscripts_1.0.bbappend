FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}-1.0:"

PRINC := "${@int(PRINC) + 1}"

do_install_append() {
	install -m 0755 ${WORKDIR}/mountdevtmpfs.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} mountdevtmpfs.sh start 02 S .

	install -m 0755 ${WORKDIR}/network.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} network.sh start 38 S .

	install -m 0755 ${WORKDIR}/httpdpasswd.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} httpdpasswd.sh start 38 S .

	install -m 0755 ${WORKDIR}/ssh_config.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} ssh_config.sh start 38 S .

	install -m 0755 ${WORKDIR}/miner_config.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} miner_config.sh start 38 S .

	install -m 0755 ${WORKDIR}/ntpdate.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} ntpdate.sh start 39 S .

	install -m 0755 ${WORKDIR}/cgminer.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} cgminer.sh start 70 S .

	cd ${D}${sysconfdir}/rcS.d
	ln -s ../init.d/ntpd S40ntpd

	install -m 0400 ${WORKDIR}/shadow.factory ${D}${sysconfdir}/shadow.factory

	install -d ${D}${base_sbindir}
	install -m 0755 ${WORKDIR}/monitordcdc ${D}${base_sbindir}/
}

SRC_URI_append = " file://mountdevtmpfs.sh"
SRC_URI_append = " file://network.sh"
SRC_URI_append = " file://httpdpasswd.sh"
SRC_URI_append = " file://ssh_config.sh"
SRC_URI_append = " file://cgminer.sh"
SRC_URI_append = " file://miner_config.sh"
SRC_URI_append = " file://ntpdate.sh"
SRC_URI_append = " file://shadow.factory"
SRC_URI_append = " file://monitordcdc"
