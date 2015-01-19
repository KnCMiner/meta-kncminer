DESCRIPTION = "BFGMiner bitcoin miner SW"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

# We need jansson library which is provided by cgminer,
# that's why cgminer is in dependencies
DEPENDS = "ncurses curl cgminer"

SRCREV = "bfgminer-5.0.0-titan-1.96"
PV = "${SRCREV}+git${SRCPV}"

SRC_URI = "git://github.com/KnCMiner/bfgminer.git;protocol=https;branch=knc"

S = "${WORKDIR}/git"

CFLAGS_prepend = "-I ${S}/uthash/src"

EXTRA_OECONF = " --enable-kncasic --disable-other-drivers "

do_configure_prepend() {
        cd ${S}
        [ -d uthash ] || git clone git://github.com/troydhanson/uthash uthash
        git tag bfgminer-5.0.0-neptune-1.04 -m "Neptune v1.04"
        ./autogen.sh
}

inherit autotools pkgconfig
