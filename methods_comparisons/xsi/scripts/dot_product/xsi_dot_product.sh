#!/bin/bash
set -euo pipefail

xsi_path="/mnt/project/methods_comparisons/xsi/ukb20279_c21_b0_v1_250129_whitelist.xsi"

# Clone
OUT_DIR=`pwd`
git clone https://github.com/rwk-unil/xSqueezeIt.git $HOME/xSqueezeIt
cd $HOME/xSqueezeIt

# Clone and build htslib (if you already have htslib set Makefile accordingly and skip)
git submodule update --init htslib
cd htslib
git submodule update --init --recursive
autoheader
autoconf
# automake --add-missing 2>/dev/null # this was throwing an error
./configure
make
sudo make install
sudo ldconfig
cd ..

# Clone, build, and install zstd (if you already have zstd set Makefile accordingly and skip)
git clone https://github.com/facebook/zstd.git
cd zstd
make
sudo make install
sudo ldconfig
cd ..

# Build application
make

# build and run dot_prod
cd $HOME/xSqueezeIt/dot_prod
make
./dot_prod -f $xsi_path