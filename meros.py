#!/usr/bin/python3


import mos.helper as helper
import mos.kernel_build as kernel_build
import mos.host_conf as host_conf
import mos.target_get as target_get
import mos.target_manage as target_manage
# import mos.libvirt_manage as libvirt_manage

import subprocess

import getopt
import sys


def main():

	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help","setup","kernel-build","get","bootstrap","build","run","shutdown","output="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print(err)  # will print something like "option -a not recognized"
		display_help()
		sys.exit(2)
	output = None
	verbose = False
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			display_help()
			sys.exit()
		elif o in ("--setup"):
			h = host_conf.HostConf()
			h.main()
			sys.exit()
		elif o in ("--kernel-build"):
			kb = kernel_build.KernelBuild
			kb.kernel_make()
			sys.exit()
		elif o in ("--get"):
			target_distro = sys.argv[2]
			tg = target_get.TargetGet(target_distro)
			tg.get_rootfs()
		elif o in ("--build"):
			target_full_id = sys.argv[2]
			tm = target_manage.TargetManage(target_full_id)
			tm.chroot_setup()
			tm.rootfs_build()
			sys.exit()
		elif o in ("--run"):
			lm = libvirt_manage.LibvirtManage()
			mos.vm_init()
			mos.net_init()
		elif o in ("--shutdown"):
			mos.run_as_root(print("Running as root"))
			mos.run_as_root(mos.vm_shutdown_all())
		elif o in ("-o", "--output"):
			output = a
		else:
			print("Error")
#			assert False, "unhandled option"

if __name__ == "__main__":
	main()



'''
--net-access)

	root_check

	declare BR_ID=$2.BR

	sys_nftables_net_access $BR_ID

	exit 0
;;
-c|--connect)

	declare VM_ID=$2

	source_vm_var
	ssh_connect

	exit 0
;;
-p|--push)

	declare FILE=$2
	declare VM_ID=$3

	ssh_push

	exit 0
;;
--pull)

	declare VM_ID=$2

	ssh_pull

	exit 0
	;;
--sync)

	declare VM_ID=$2

	ssh_sync

	exit 0
;;
--clean)

	root_check

	rm -rf $MOS_PATH/etc/build/kernel/*
	rm -rf $MOS_PATH/etc/build/bootstrap/*

	exit 0
;;
'''
