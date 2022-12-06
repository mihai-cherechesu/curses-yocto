FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://hostname \
	   "
do_install_append () {
	install -m 0644 ${WORKDIR}/hostname ${D}${sysconfdir}
}
