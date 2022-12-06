#!/bin/bash
if [ "$EUID" -ne 0 ]; then echo "Please run as root!" >&2; exit 1; fi
if ! command -v brctl &>/dev/null; then echo "Please install bridge-utils!"; exit 1; fi

# Creaza un bridge (virbr0) la interfața externă a mașinii virtuale
NET_INTERFACE=$1   # first argument to override
if [[ -z "$NET_INTERFACE" ]]; then
	NET_INTERFACE=$(ip link | awk -F: '$0 !~ "lo|vir|wl|^[^0-9]"{print $2;getline}' | xargs)
	[[ -n "$NET_INTERFACE" ]] || { echo "Could not autodetect net iface!"; exit 1; }
fi
brctl addbr virbr0
brctl addif virbr0 "$NET_INTERFACE"
ip address flush dev "$NET_INTERFACE"
ip address flush dev "virbr0"
dhclient "virbr0"

mkdir -p /etc/qemu/
echo "allow virbr0" > /etc/qemu/bridge.conf

# don't use this on your host system, it may be potentially insecure!
sudo chmod u+s /usr/lib/qemu/qemu-bridge-helper

