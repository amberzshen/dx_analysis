#!/bin/bash

# download python 3.10
sudo apt update
sudo apt install libffi-dev
curl https://pyenv.run | bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv install 3.10.13
pyenv global 3.10.13

pip install h5py
pip install polars
pip install memory_profiler
pip install git+https://github.com/quattro/linear-dag.git

# install latest grgl version
git clone --recursive https://github.com/aprilweilab/grgl.git
cd grgl
pip install .
cd ..

python get_matmat_time.py