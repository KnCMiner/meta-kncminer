DESCRIPTION = "BFGMiner bitcoin miner SW"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

# We need jansson library which is provided by cgminer,
# that's why cgminer is in dependencies
DEPENDS = "ncurses curl cgminer"

SRCREV = "bfgminer-3.8.1"
PV = "${SRCREV}+git${SRCPV}"

SRC_URI = "git://github.com/luke-jr/bfgminer.git;protocol=https;branch=bfgminer"

SRC_URI_append = " file://knc-spidevc-fix.patch \
				 "

S = "${WORKDIR}/git"

CFLAGS_prepend = "-I ${S}/uthash/src"

EXTRA_OECONF = " \
		--disable-bitforce --disable-icarus --disable-avalon --disable-modminer \
		--disable-klondike --disable-x6500 --disable-ztex --disable-bifury \
		--disable-bitfury --disable-bigpic --disable-twinfury \
		--disable-littlefury --disable-nanofury --disable-hashbuster \
		--disable-hashbusterusb \
		--without-libusb \
		--enable-knc \
		"

do_configure_prepend() {
        cd ${S}
        [ -d uthash ] || git clone git://github.com/troydhanson/uthash uthash
        ./autogen.sh
}

inherit autotools pkgconfig
