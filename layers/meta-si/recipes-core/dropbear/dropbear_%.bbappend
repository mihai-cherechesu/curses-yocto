do_install_append(){
    sed -i 's/-w//g' ${D}/etc/default/dropbear
}