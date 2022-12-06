FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://avahi-daemon.conf \
    "

do_install_append() {
    install -d ${D}${sysconfdir}/avahi
    install -m 644 ${WORKDIR}/avahi-daemon.conf ${D}${sysconfdir}/avahi
}