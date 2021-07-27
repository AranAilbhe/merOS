#!/usr/bin/python3

import os
import sys
import mos
from mos.helper import *
from mos.bootstrap import *

from shutil import *
import distutils
from distutils import *
from distutils import dir_util
import subprocess
from os import chmod
from Crypto.PublicKey import RSA

target_chroot_conf_dir = mos.mos_path + "/conf/" + target_distro + "/" + mos.target_id + "/includes.chroot"
target_chroot_dir = mos.mos_path + "/data/build/bootstrap/" + target_distro + "/" + mos.target_id

target_ssh_dir = target_chroot_dir + "/etc/ssh"

def target_chroot_build():

	if os.path.isdir(target_chroot_dir):
		None
	else:
		os.makedirs(target_chroot_dir, mode = 0o777, exist_ok = True)

		tar_file = tarfile.open(rootfs_targz)
		tar_file.extractall(target_chroot_dir)
		tar_file.close

	distutils.dir_util.copy_tree(target_chroot_conf_dir, target_chroot_dir)


def gen_ssh_keys():

	key = RSA.generate(2048)

	if not os.path.exists(target_ssh_dir):
		os.makedirs(target_ssh_dir)
	else:
		None

	## Write Target host key
	with open(target_ssh_dir + "/ssh_host_rsa_key", 'wb') as content_file:
		chmod(target_ssh_dir + "/ssh_host_rsa_key", 0o0600)
		content_file.write(key.exportKey('PEM'))

	## Write mos authentication pair
	with open(mos_ssh_priv_key_dir + "/" + mos.target_id + "-id_rsa", 'wb') as content_file:
		chmod(mos_ssh_priv_key_dir + "/" + mos.target_id + "-id_rsa", 0o0600)
		content_file.write(key.exportKey('PEM'))
		pubkey = key.publickey()
	with open(target_ssh_dir + "/authorized_keys", 'wb') as content_file:
		content_file.write(pubkey.exportKey('OpenSSH'))


def chroot_configure():
	os.chroot(target_chroot_dir)
	with open("/etc/resolv.conf", 'w') as file:
		file.write("nameserver " + default_gw + "\n")

	subprocess.run("/root/0100-conf.chroot", shell=True)
	subprocess.run("/root/0150-packages.chroot", shell=True)

## TODO ssh-keygen -f "/home/$USER_ID/.ssh/known_hosts" -R "[10.0.4.4]:2022" TODO
