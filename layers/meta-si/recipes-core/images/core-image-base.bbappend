IMAGE_INSTALL += "packagegroup-core-ssh-dropbear yellow-submarine dotfiles"

inherit extrausers

EXTRA_USERS_PARAMS += "usermod -P labsi root;"
