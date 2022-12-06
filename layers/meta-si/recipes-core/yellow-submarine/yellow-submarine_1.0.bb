SUMMARY = "yellow-submarine recipe"
DESCRIPTION = "Python curses based drawer app"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${WORKDIR}/LICENSE;md5=4ee23c52855c222cba72583d301d2338"

FILESEXTRAPATHS_prepend = "${THISDIR}/${PN}:"

SRC_URI = " \
    file://app.py \
    file://db.py \
    file://vincent_van_gogu.py \
    file://wsgi.py \
    file://LICENSE \
    "

RDEPENDS_${PN} += "python3-flask python3-curses python3-pip python3-gunicorn"

FILES_${PN} = "/app/*.py"
do_install() {
    install -d ${D}/app
    install -m 0755 ${WORKDIR}/wsgi.py ${D}/app/wsgi.py
    install -m 0755 ${WORKDIR}/app.py ${D}/app/app.py
    install -m 0755 ${WORKDIR}/db.py ${D}/app/db.py
    install -m 0755 ${WORKDIR}/vincent_van_gogu.py ${D}/app/vincent_van_gogu.py
}