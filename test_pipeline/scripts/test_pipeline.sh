kodama make-geno \
    --vcf_path "/Users/ambershen/Desktop/linARG/data/1kg/CCDG_14151_B01_GRM_WGS_2020-08-05_chr6.filtered.shapeit2-duohmm-phased.vcf.gz" \
    --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/save/" \
    --region "chr6-32578775-33578776" \
    --partition_number 0 \
    --phased \
    --flip_minor_alleles \
    --maf_filter 0.1

# kodama run-forward-backward --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/save/" --partition_identifier 0_chr6-32578775-33578775

# kodama reduction-union-recom --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/save/" --partition_identifier 0_chr6-32578775-33578775

# kodama merge --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/save/"



# kodama make-geno \
#     --vcf_path "/Users/ambershen/Desktop/linARG/data/1kg/CCDG_14151_B01_GRM_WGS_2020-08-05_chr6.filtered.shapeit2-duohmm-phased.vcf.gz" \
#     --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/no_save/" \
#     --region "chr6-32578775-33578775" \
#     --partition_number 0 \
#     --phased \
#     --flip_minor_alleles \

# kodama infer-brick-graph --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/no_save/" --partition_identifier 0_chr6-32578775-33578775



# kodama merge --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/no_save/"
