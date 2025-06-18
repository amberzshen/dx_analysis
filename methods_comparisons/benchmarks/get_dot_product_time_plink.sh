#!/bin/bash
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

vcf_path="/mnt/project/amber/filtered_vcfs/ukb20279_c${chrom}_b0_v1_250129_whitelist.vcf.gz"
python /mnt/project/amber/scripts/make_weights.py $chrom
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/dot_product_plink_chr${chrom}.csv plink2 --vcf $vcf_path --score weights.txt list-variants --set-all-var-ids @:#:\$r:\$a --out chr${chrom}_scores --new-id-max-allele-len 1000 missing