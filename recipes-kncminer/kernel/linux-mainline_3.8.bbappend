FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "file://defconfig \
			"

do_deploy_append() {
	install -d ${DEPLOY_DIR_IMAGE}
	cp -p ${D}/boot/*.dtb ${DEPLOY_DIR_IMAGE}/.
}
