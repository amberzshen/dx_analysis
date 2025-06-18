#!/bin/bash
set -euo pipefail
chrom=$1

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

vcf_path="/mnt/project/amber/filtered_vcfs/ukb20279_c${chrom}_b0_v1_250129_whitelist.vcf.gz"
python /mnt/project/amber/scripts/make_phenotypes.py
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/gwas_plink_chr${chrom}.csv \
    plink2 --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
    --double-id \
    --no-input-missing-phenotype \
    --pheno phenotypes.txt --pheno-name p50_i0 \
    --covar covariates.txt --covar-name intercept,p21022,p31,$(printf "p22009_a%d," {1..40} | sed 's/,$//') \
    --glm hide-covar \
    --out chr${chrom}_gwas