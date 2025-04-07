#!/bin/bash
set -euo pipefail

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
pip install git+https://github.com/quattro/linear-dag.git
python linarg_to_mtx.py

gunzip 1kg_chr1_julia.psam.gz
gunzip 1kg_chr1_julia.pvar.gz