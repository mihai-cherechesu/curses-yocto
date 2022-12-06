#!/bin/bash
IMAGE_FILE="rootfs.img"
KERNEL_FILE="kernel-yocto"
DEVICE_TREE="versatile-pb.dtb"

# to make the script usable from source dir, use after calling `make bin_archive`
BIN_TMP_DIR="build/tmp/bin_archive/"
if [[ -d "$BIN_TMP_DIR" ]]; then cd "$BIN_TMP_DIR"; fi

# disable audio (for qemu 2.x)
export QEMU_AUDIO_DRV=none

QEMU_ARGS=( # yep, this is a bash array
	# NOTE: use Qemu machine type 'virt' instead of 'versatilepb' for
	# compatibility with Yocto's 'qemuarm' arch; also, this doesn't require
	# a device tree ;)
	-machine virt,highmem=off -cpu cortex-a15 -m 256
	-drive "file=$IMAGE_FILE,if=none,media=disk,format=raw,id=disk0"
	-device "virtio-blk-pci,drive=disk0,disable-modern=on"
	-kernel "$KERNEL_FILE"
	-append "root=/dev/vda rw panic=1 console=ttyAMA0"
	-serial stdio -nographic
	-monitor telnet::45454,server,nowait
	-no-reboot
)

# use bridging with virbr0
QEMU_ARGS+=(-net bridge,br=virbr0 -net nic,model=virtio)

exec qemu-system-arm "${QEMU_ARGS[@]}"

