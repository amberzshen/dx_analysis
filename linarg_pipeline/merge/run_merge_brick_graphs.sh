#!/bin/bash
data_identifier=$1

# download python 3.9 and cython complier dependencies
sudo apt-get update
sudo apt -y install python3.9
sudo apt -y install python3.9-dev
python3.9 -m pip install --upgrade pip

python3.9 -m pip install --upgrade scipy
python3.9 -m pip install cyvcf2
python3.9 -m pip install dxpy # for dna_nexus.py
python3.9 -m pip install pyspark # for dna_nexus.py
python3.9 -m pip install git+https://github.com/quattro/linear-dag.git@amber_debug

mkdir -p $data_identifier

python3.9 merge_brick_graphs.py $data_identifier
