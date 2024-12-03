#!/bin/bash
linarg_dir=$1
beta_dir=$2
partition_id=$3
out_dir=$4

set -euo pipefail

sudo apt update
sudo apt install libffi-dev
curl https://pyenv.run | bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv install 3.10.0
pyenv global 3.10.0

pip install --upgrade pip
pip install --upgrade scipy
pip install cyvcf2
pip install pandas
pip install git+https://github.com/quattro/linear-dag.git@bed_reader_removed

python process_beta_hats.py $linarg_dir $beta_dir $partition_id $out_dir