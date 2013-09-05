DESCRIPTION = "Device tree binary for Beagle bone in Kncminers"
LICENSE = "unknown"
LIC_FILES_CHKSUM = "file://COPYING;md5=d41d8cd98f00b204e9800998ecf8427e"

SRC_URI = " file://am335x-boneblack.dts"
SRC_URI_append = " file://am335x-bone-common.dtsi"
SRC_URI_append = " file://am335x-bone-knc.dtsi"
SRC_URI_append = " file://am33xx.dtsi"
SRC_URI_append = " file://skeleton.dtsi"
SRC_URI_append = " file://tps65217.dtsi"
SRC_URI_append = " file://COPYING"

S = "${WORKDIR}"

do_compile() {
	dtc am335x-boneblack.dts -O dtb -o am335x-boneblack-kncminer.dtb
}

do_install() {
	cp -p *.dtb ${DEPLOY_DIR_IMAGE}/.
}
