# Makefile pentru generarea arhivelor sursa / binare

# numele artefactului Yocto care va genera imaginea
# ATENTIE: MODIFICATI daca folositi alt target / machine Yocto !
YOCTO_ARTIFACT = core-image-base
YOCTO_MACHINE = qemuarm
# unde sa se genereze arhiva cu binarele
BIN_TMP_DIR = build/tmp/bin_archive

_YOCTO_IMAGE_DIR = build/tmp/deploy/images/$(YOCTO_MACHINE)
bin_archive:
	@if ! command -v zip &>/dev/null; then echo "Please install zip!"; exit 1; fi
	@mkdir -p "$(BIN_TMP_DIR)/"
	cp -f "$(_YOCTO_IMAGE_DIR)/zImage" "$(BIN_TMP_DIR)/kernel-yocto"
	cp -f "$(_YOCTO_IMAGE_DIR)/$(YOCTO_ARTIFACT)-$(YOCTO_MACHINE).ext4" \
		"$(BIN_TMP_DIR)/rootfs.img"
	cp -f launch.sh "$(BIN_TMP_DIR)/"
	cp -f test.sh "$(BIN_TMP_DIR)/"
	tar czvf bin_archive.tar.gz -C "$(BIN_TMP_DIR)/" .

bin_checksum:
	sha256sum bin_archive.tar.gz > CHECKSUM
	cat CHECKSUM

source_archive:
	@if ! command -v zip &>/dev/null; then echo "Please install zip!"; exit 1; fi
	@rm -f "source_archive.zip"
	zip -r -y source_archive.zip . -x '*.zip' -x '*.tar.gz' -x 'build/*' -x 'layers/*'

.PHONY: bin_archive bin_checksum source_archive

