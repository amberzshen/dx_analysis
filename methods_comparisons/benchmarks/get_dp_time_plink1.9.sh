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

# python /mnt/project/amber/scripts/make_phenotypes.py
python /mnt/project/amber/scripts/make_weights.py $chrom

# bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/convert_vcf_to_pgen_plink_chr${chrom}.csv \
    # plink \
    #     --vcf $vcf_path \
    #     --make-bed \
    #     --double-id \
    #     --new-id-max-allele-len 1000 \
    #     --out ukb20279_c${chrom}_b0_v1_250129_whitelist

# bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/gwas_plink_chr${chrom}.csv \
#     plink \
#     --bfile ukb20279_c${chrom}_b0_v1_250129_whitelist \
#     --pheno phenotypes.txt --pheno-name p50_i0 \
#     --covar covariates.txt --covar-name intercept,p21022,p31,$(printf "p22009_a%d," {1..40} | sed 's/,$//') \
#     --linear hide-covar \
#     --out chr${chrom}_gwas_plink1.9

bcftools annotate \
    -x ID \
    -I +'%CHROM:%POS:%REF:%ALT' \
    --rename-chr <(echo "chr${chrom} ${chrom}" ) \
    -o renamed.vcf.gz \
    -O z \
    $vcf_path


bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/plink_dot_product_chr${chrom}.csv \
    plink \
        --vcf renamed.vcf.gz \
        --score weights.txt 1 2 3 sum \
        --double-id \
        --new-id-max-allele-len 1000 \
        --out tmp

# rm phenotypes.txt
# rm covariates.txt
rm weights.txt