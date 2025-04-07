# Clone
git clone https://github.com/rwk-unil/xSqueezeIt.git
cd xSqueezeIt

# Clone and build htslib (if you already have htslib set Makefile accordingly and skip)
git submodule update --init htslib
cd htslib
git submodule update --init --recursive
autoheader
autoconf
automake --add-missing 2>/dev/null
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