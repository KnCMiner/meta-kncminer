meta-kncminer
=============

OpenEmbedded / Ångström meta layer for KnCMiner

Setup instructoins
------------------

To build a KnCMiner firmware, first prepare a build machine as per OpenEmbedded Required software instructions at http://www.openembedded.org/wiki/Getting_started

When machine is prepared proceed to prepare the KnCMiner firmware build by running

    git clone https://github.com/KnCMiner/setup-scripts.git
    cd setup-scripts
    MACHINE=beaglebone ./oebb.sh configure beaglebone

Rootfs build instructions
----------------------------------
  
To build the firmware rootfs run

    . environment-angstrom-v2013.06
    bitbake kncminer

and then wait for quite a bit for the build to complete.

Note: You will need ~11GB free disk space.

The resulting root initramfs will be in

    setup-scripts/deploy/eglibc/images/beaglebone/Angstrom-kncminer-eglibc-ipk-v2013.06-beaglebone.rootfs.cpio.gz.u-boot


Kernel build instructions
-----------------------------------

To build the Linux kernel image run

    . environment-angstrom-v2013.06
    bitbake virtual/kernel

which results in a kernel image at

    setup-scripts/deploy/eglibc/images/beaglebone/
