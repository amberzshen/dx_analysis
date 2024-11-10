#!/bin/bash
res_dir=$1
load_dir=$2
graph_type=$3
start=$4
end=$5

# mtx_path=$1
# variant_path=$2
# out=$3

set -euo pipefail

# download python 3.9 and cython complier dependencies
sudo apt-get update
sudo apt -y install python3.9
sudo apt -y install python3.9-dev
python3.9 -m pip install --upgrade pip

python3.9 -m pip install --upgrade scipy
python3.9 -m pip install cyvcf2
python3.9 -m pip install dxpy # for dna_nexus.py
python3.9 -m pip install pyspark # for dna_nexus.py
python3.9 -m pip install git+https://github.com/quattro/linear-dag.git

# mkdir -p $out
mkdir -p $res_dir

export PATH=$PATH:/home/dnanexus/.local/bin/
# python3.9 debug_counts.py $mtx_path $variant_path $out
python3.9 debug_counts.py $res_dir $load_dir $graph_type $start $end