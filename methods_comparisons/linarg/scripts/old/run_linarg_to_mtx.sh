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

gunzip 0_chr21-5030618-25863389_julia.psam.gz
gunzip 0_chr21-5030618-25863389_julia.pvar.gz

gunzip 1_chr21-25863390-46696162_julia.psam.gz
gunzip 1_chr21-25863390-46696162_julia.pvar.gz