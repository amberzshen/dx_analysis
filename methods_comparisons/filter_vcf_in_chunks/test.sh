vcf_path="/Users/ambershen/Desktop/linARG/data/1kg/CCDG_14151_B01_GRM_WGS_2020-08-05_chr6.filtered.shapeit2-duohmm-phased.vcf.gz"
out="/Users/ambershen/Desktop/linARG/dx_analysis/methods_comparisons/filter_vcf_in_chunks/test/chr6_test.vcf.gz"
bcftools view --regions-overlap 0 --regions "chr6:32578775-33578776" -Oz -o "$out" "$vcf_path"
bcftools index $out

kodama make-geno \
    --vcf_path "/Users/ambershen/Desktop/linARG/dx_analysis/methods_comparisons/filter_vcf_in_chunks/test/chr6_test.vcf.gz" \
    --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/methods_comparisons/filter_vcf_in_chunks/test/" \
    --region "chr6-32578775-33578776" \
    --partition_number "test" \
    --phased \
    --flip_minor_alleles \


kodama make-geno \
    --vcf_path "/Users/ambershen/Desktop/linARG/dx_analysis/methods_comparisons/filter_vcf_in_chunks/test/chr6.vcf.gz" \
    --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/methods_comparisons/filter_vcf_in_chunks/test" \
    --region "chr6-32578775-33578776" \
    --partition_number "output" \
    --phased \
    --flip_minor_alleles \
