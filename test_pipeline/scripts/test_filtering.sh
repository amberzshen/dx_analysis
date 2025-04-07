kodama make-geno \
    --vcf_path "/Users/ambershen/Desktop/linARG/data/1kg/CCDG_14151_B01_GRM_WGS_2020-08-05_chr6.filtered.shapeit2-duohmm-phased.vcf.gz" \
    --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/maf_filter_0.05/" \
    --region "chr6-32578775-33578775" \
    --partition_number 0 \
    --phased \
    --flip_minor_alleles \
    --maf_filter 0.05

kodama run-forward-backward --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/maf_filter_0.05/" --partition_identifier 0_chr6-32578775-33578775

kodama reduction-union-recom --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/maf_filter_0.05/" --partition_identifier 0_chr6-32578775-33578775

kodama merge --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/maf_filter_0.05/"


kodama make-geno \
    --vcf_path "/Users/ambershen/Desktop/linARG/data/1kg/CCDG_14151_B01_GRM_WGS_2020-08-05_chr6.filtered.shapeit2-duohmm-phased.vcf.gz" \
    --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/maf_filter_0.05_indels_removed/" \
    --region "chr6-32578775-33578775" \
    --partition_number 0 \
    --phased \
    --flip_minor_alleles \
    --maf_filter 0.05 \
    --remove_indels

kodama run-forward-backward --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/maf_filter_0.05_indels_removed/" --partition_identifier 0_chr6-32578775-33578775

kodama reduction-union-recom --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/maf_filter_0.05_indels_removed/" --partition_identifier 0_chr6-32578775-33578775

kodama merge --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/maf_filter_0.05_indels_removed/"


kodama make-geno \
    --vcf_path "/Users/ambershen/Desktop/linARG/data/1kg/CCDG_14151_B01_GRM_WGS_2020-08-05_chr6.filtered.shapeit2-duohmm-phased.vcf.gz" \
    --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/no_filter/" \
    --region "chr6-32578775-33578775" \
    --partition_number 0 \
    --phased \
    --flip_minor_alleles

kodama run-forward-backward --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/no_filter/" --partition_identifier 0_chr6-32578775-33578775

kodama reduction-union-recom --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/no_filter/" --partition_identifier 0_chr6-32578775-33578775

kodama merge --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/no_filter/"