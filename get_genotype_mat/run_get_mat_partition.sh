#!/bin/bash

set -euo pipefail

region=$1
out_prefix=$2

mkdir -p matrices
mkdir -p variant_metadata

pip install --upgrade scipy
pip install cyvcf2
python3 get_mat.py $region $out_prefix