#!/bin/bash
linarg_dir=$1
partition_id=$2
data_type=$3
res_dir=$4

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

python lin_reg_height_w_covariates.py $linarg_dir $partition_id $data_type $res_dir