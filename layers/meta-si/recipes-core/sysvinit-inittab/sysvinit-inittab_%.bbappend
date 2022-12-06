do_install_append() {
    sed -i -e 's/^\(AMA0.*\)vt102/\1xterm-256color/' ${D}${sysconfdir}/inittab
}