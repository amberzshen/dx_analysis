#!/bin/bash
linarg_dir=$1
load_dir=$2

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
pip install git+https://github.com/quattro/linear-dag.git@forward_backward_to_disk
kodama merge --linarg_dir $linarg_dir --load_dir $load_dir