#!/bin/bash

### testing ###
# partition_dir="/Users/ambershen/Desktop/linARG/dx_analysis/methods_comparisons/filter_vcf_in_chunks/test/partitions"
# out="/Users/ambershen/Desktop/linARG/dx_analysis/methods_comparisons/filter_vcf_in_chunks/test/chr6.vcf.gz"

partition_dir="/mnt/project/amber/filtered_vcfs/chr1/"
out="ukb20279_c1_b0_v1_250129_whitelist.vcf.gz"

partitions="partition_paths.txt"
find "$partition_dir" -type f | sort -V > "$partitions"
bcftools concat --file-list $partitions -n -o $out
bcftools index $out

rm $partitions
