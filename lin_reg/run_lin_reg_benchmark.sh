#!/bin/bash
linarg_dir=$1
partition_id=$2
data_type=$3
res_dir=$4

set -euo pipefail

sudo apt-get update
sudo apt -y install python3.9
sudo apt -y install python3.9-dev
python3.9 -m pip install --upgrade pip

python3.9 -m pip install --upgrade scipy
python3.9 -m pip install cyvcf2
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o rustup_installer.sh
sh rustup_installer.sh -y
exec bash
python3.9 -m pip install git+https://github.com/quattro/linear-dag.git

python3.9 lin_reg_benchmark.py $linarg_dir $partition_id $data_type $res_dir
