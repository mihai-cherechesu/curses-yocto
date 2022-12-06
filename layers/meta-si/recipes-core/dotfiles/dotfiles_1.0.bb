SUMMARY = "Environment customizations"
DESCRIPTION = "Dotfiles such as .bashrc for the root user"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${WORKDIR}/LICENSE;md5=4ee23c52855c222cba72583d301d2338"

FILESEXTRAPATHS_prepend = "${THISDIR}/${PN}:"

SRC_URI = " \
    file://bashrc_root \
    file://profile_root \
    file://LICENSE \
    "

FILES_${PN} += "/home/root/.*"
do_install() {
    install -d ${D}/home/root
    install -m 0755 ${WORKDIR}/profile_root ${D}/home/root/.profile
    install -m 0755 ${WORKDIR}/bashrc_root ${D}/home/root/.bashrc
}