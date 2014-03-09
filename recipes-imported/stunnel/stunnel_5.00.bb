SUMMARY = "SSL encryption wrapper between remote client and local (inetd-startable) or remote server."
SECTION = "net"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=45e8e7befe9a0f7e0543b78dfeebde20"
DEPENDS = "openssl"

SRC_URI = "https://www.stunnel.org/downloads/${BP}.tar.gz"

SRC_URI[md5sum] = "4f00fd0faf99e3c9cf258a19dd83d14a"
SRC_URI[sha256sum] = "88986d52a7ef1aff0cc26fc0a9830361c991baba7ee591d5cf1cc8baef75bc13"

inherit autotools

EXTRA_OECONF += "--with-ssl='${STAGING_INCDIR}' --disable-fips"
