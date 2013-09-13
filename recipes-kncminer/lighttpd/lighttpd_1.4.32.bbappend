FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}-1.0:"

PRINC := "${@int(PRINC) + 1}"

RDEPENDS_${PN} += " \
               lighttpd-module-auth \
               lighttpd-module-cgi \
"

do_install_append() {
    update-rc.d -r ${D} lighttpd start 60 S .
    install -m 0755 ${WORKDIR}/lighttpd.conf ${D}${sysconfdir}
    install -m 0755 ${WORKDIR}/lighttpd-htdigest.user ${D}${sysconfdir}
    cp -pr ${WORKDIR}/www/* ${D}/www/pages
#    cp -pr ${WORKDIR}/cgi ${D}/www/pages
}

SRC_URI_append = " file://lighttpd.conf"
#SRC_URI_append = " file://index.html.lighttpd"
SRC_URI_append = " file://lighttpd-htdigest.user"
SRC_URI_append = " file://www"
#SRC_URI_append = " file://cgi"
