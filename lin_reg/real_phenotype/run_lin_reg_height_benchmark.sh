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

python lin_reg_height_benchmark.py $linarg_dir $partition_id $data_type $res_dir



# python3.9 -m pip install scipy==1.14.0

# sudo apt-get update
# sudo apt -y install python3.9
# sudo apt -y install python3.9-dev
# python3.9 -m pip install --upgrade pip

# python3.9 -m pip install --upgrade scipy
# python3.9 -m pip install cyvcf2
# python3.9 -m pip install pandas

# python3.9 -m pip install git+https://github.com/quattro/linear-dag.git@bed_reader_removed
# python3.9 lin_reg_height_benchmark.py $linarg_dir $partition_id $data_type $res_dir