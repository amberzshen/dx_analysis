#!/bin/bash

set -euo pipefail

chrom=$1
region=$2
out_prefix=$3

vcf_file="/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c${chrom}_b0_v1.vcf.gz"

mkdir -p tmp
mkdir -p genotype_matrices/matrices
mkdir -p genotype_matrices/variant_metadata

pip install --upgrade scipy
pip install cyvcf2
bcftools view -Ob -r $region "$vcf_file" > "tmp/${out_prefix}_${region}.bcf" # stream region of chromosome to worker
python3 get_mat.py $region $out_prefix

rm -r tmp
