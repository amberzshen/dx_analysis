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

python /mnt/project/amber/scripts/make_weights_multcols.py $chrom 1
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/plink2_matmat_chr${chrom}_1.csv \
    plink2 \
        --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
        --score weights_1.txt \
        --out tmp

python /mnt/project/amber/scripts/make_weights_multcols.py $chrom 2
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/plink2_matmat_chr${chrom}_2.csv \
    plink2 \
        --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
        --score weights_2.txt \
        --score-col-nums 3-4 \
        --out tmp

python /mnt/project/amber/scripts/make_weights_multcols.py $chrom 10
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/plink2_matmat_chr${chrom}_10.csv \
    plink2 \
        --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
        --score weights_10.txt \
        --score-col-nums 3-12 \
        --out tmp

python /mnt/project/amber/scripts/make_weights_multcols.py $chrom 20
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/plink2_matmat_chr${chrom}_20.csv \
    plink2 \
        --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
        --score weights_20.txt \
        --score-col-nums 3-22 \
        --out tmp

python /mnt/project/amber/scripts/make_weights_multcols.py $chrom 40
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/plink2_matmat_chr${chrom}_40.csv \
    plink2 \
        --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
        --score weights_20.txt \
        --score-col-nums 3-42 \
        --out tmp

python /mnt/project/amber/scripts/make_weights_multcols.py $chrom 60
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/plink2_matmat_chr${chrom}_60.csv \
    plink2 \
        --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
        --score weights_60.txt \
        --score-col-nums 3-62 \
        --out tmp

python /mnt/project/amber/scripts/make_weights_multcols.py $chrom 80
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/plink2_matmat_chr${chrom}_80.csv \
    plink2 \
        --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
        --score weights_80.txt \
        --score-col-nums 3-82 \
        --out tmp

python /mnt/project/amber/scripts/make_weights_multcols.py $chrom 100
bash /mnt/project/amber/scripts/profile.sh $OUT_DIR/plink2_matmat_chr${chrom}_100.csv \
    plink2 \
        --pfile /mnt/project/amber/methods_comparisons/results/ukb20279_c${chrom}_b0_v1_250129_whitelist \
        --score weights_100.txt \
        --score-col-nums 3-102 \
        --out tmp

rm weights*
rm tmp*