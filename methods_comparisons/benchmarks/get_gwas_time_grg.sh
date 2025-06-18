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

pip install pygrgl
pip install numpy
pip install polars

grg_path="/mnt/project/methods_comparisons/grg/ukb20279_c${chrom}_b0_v1_250129_whitelist.grg"
python /mnt/project/amber/scripts/make_phenotypes_fill_null.py
tail -n +2 phenotypes.txt > phenotypes_no_header.txt
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/gwas_grg_chr${chrom}.csv \
    grg process gwas $grg_path --phenotype phenotypes_no_header.txt