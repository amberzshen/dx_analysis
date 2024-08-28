#!/bin/bash

set -euo pipefail

region=$1
out_prefix=$2

mkdir -p genotype_matrices
mkdir -p variant_metadata

pip install --upgrade scipy
pip install cyvcf2
python3 get_mat_partition.py $region $out_prefix