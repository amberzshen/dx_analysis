#!/bin/bash
vcf_path=$1
linarg_dir=$2
region=$3
partition_number=$4

set -euo pipefail

# download python 3.9 and cython complier dependencies
sudo apt-get update
sudo apt -y install python3.9
sudo apt -y install python3.9-dev
python3.9 -m pip install --upgrade pip

python3.9 -m pip install --upgrade scipy
python3.9 -m pip install pandas
python3.9 -m pip install cyvcf2

python3.9 get_geno_filter.py "$vcf_path" $linarg_dir $region $partition_number