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


plink2  \
    --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
    --hardy \
    --autosome \
    --seed 111 --threads 1 --memory 8000 require \
    --out chr${chrom}_hwe
