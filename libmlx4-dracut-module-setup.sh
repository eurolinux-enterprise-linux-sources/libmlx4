#!/bin/bash

check() {
	if [ -n "$hostonly" ]; then
		lspci | grep Mellanox | grep ConnectX &>/dev/null
		return $?
	fi
	return 0
}

depends() {
	echo "rdma"
}

install() {
	inst /etc/rdma/mlx4.conf
	inst /usr/libexec/setup-mlx4.sh
	inst /etc/modprobe.d/libmlx4.conf
	inst_multiple sleep
	inst_multiple -o /etc/modprobe.d/mlx4.conf
}

installkernel() {
	instmods mlx4_core mlx4_en mlx4_ib
}

