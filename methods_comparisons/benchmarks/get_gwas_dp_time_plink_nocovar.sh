#!/bin/bash
set -euo pipefail

chrom=21

OUT_DIR=`pwd`

# download python 3.10
sudo apt update
sudo apt install libffi-dev
curl https://pyenv.run | bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv install 3.10.13
pyenv global 3.10.13

pip install h5py
pip install numpy
pip install polars

python /mnt/project/amber/scripts/make_phenotypes_nocovar.py

plink2 \
    --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
    --no-input-missing-phenotype \
    --pheno phenotypes.txt --pheno-name p50_i0 \
    --covar covariates.txt --covar-name intercept \
    --glm hide-covar \
    --out chr${chrom}_gwas_nocovar

rm phenotypes.txt
rm covariates.txt