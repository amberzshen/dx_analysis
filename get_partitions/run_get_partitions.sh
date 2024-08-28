#!/bin/bash

set -euo pipefail

region=$1
window_size=$2

pip install cyvcf2
pip install numpy
python3 get_partitions.py $region $window_size