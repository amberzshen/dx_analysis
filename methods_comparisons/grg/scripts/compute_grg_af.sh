#!/bin/bash
grg_path="ukb20279_c21_b0_v1_250129_whitelist.grg"

# download python 3.10
sudo apt update
sudo apt install libffi-dev
curl https://pyenv.run | bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv install 3.10.13
pyenv global 3.10.13 

pip install pygrgl

grg process freq $grg_path
