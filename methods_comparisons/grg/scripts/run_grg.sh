#!/bin/bash
igd_path="/mnt/project/methods_comparisons/grg/ukb20279_c21_b0_v1_250129_whitelist.igd"
out="ukb20279_c21_b0_v1_250129_whitelist.grg"

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

grg construct $igd_path -o $out --maf-flip --jobs 70 --trees 4 --parts 70 > construction.c21.log
# grg construct $igd_path -o $out --jobs 72 --trees 280 --parts 70
