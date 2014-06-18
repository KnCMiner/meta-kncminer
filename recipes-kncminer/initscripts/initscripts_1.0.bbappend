FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}-1.0:"

PRINC := "${@int(PRINC) + 1}"

do_install_append() {
	install -m 0755 ${WORKDIR}/mountdevtmpfs.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} mountdevtmpfs.sh start 02 S .

	install -m 0755 ${WORKDIR}/network.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} network.sh start 38 S .

	install -m 0755 ${WORKDIR}/kncminer_setup.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} kncminer_setup.sh start 38 S .

	install -m 0755 ${WORKDIR}/initc.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} initc.sh start 65 S .

	install -m 0755 ${WORKDIR}/ntpdate.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} ntpdate.sh start 39 S .

	install -m 0755 ${WORKDIR}/cgminer.sh ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} cgminer.sh start 70 S .

	cd ${D}${sysconfdir}/rcS.d
	ln -s ../init.d/ntpd S40ntpd

	install -m 0400 ${WORKDIR}/shadow.factory ${D}${sysconfdir}/shadow.factory

	install -d ${D}${base_sbindir}
	install -m 0755 ${WORKDIR}/monitordcdc ${D}${base_sbindir}/
	install -m 0755 ${WORKDIR}/monitordcdc.ge ${D}${base_sbindir}/
	install -m 0755 ${WORKDIR}/monitordcdc.ericsson ${D}${base_sbindir}/
	install -m 0755 ${WORKDIR}/factory_setup ${D}${base_sbindir}/

	install -m 0755 ${WORKDIR}/firewall_setup ${D}${sysconfdir}
	install -d ${D}${sysconfdir}/udhcpc.d
	install -m 0755 ${WORKDIR}/90firewall ${D}${sysconfdir}/udhcpc.d
}

SRC_URI_append = " file://mountdevtmpfs.sh"
SRC_URI_append = " file://network.sh"
SRC_URI_append = " file://initc.sh"
SRC_URI_append = " file://cgminer.sh"
SRC_URI_append = " file://ntpdate.sh"
SRC_URI_append = " file://shadow.factory"
SRC_URI_append = " file://kncminer_setup.sh"
SRC_URI_append = " file://monitordcdc"
SRC_URI_append = " file://monitordcdc.ge"
SRC_URI_append = " file://monitordcdc.ericsson"
SRC_URI_append = " file://firewall_setup"
SRC_URI_append = " file://90firewall"
SRC_URI_append = " file://factory_setup"
