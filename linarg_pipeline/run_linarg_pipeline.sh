#!/bin/bash
data_identifier=$1

pip install --upgrade scipy
pip install cyvcf2
pip install git+https://github.com/quattro/linear-dag.git
python3 linarg_pipeline.py $data_identifier