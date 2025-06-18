kodama make-geno \
    --vcf_path "/Users/ambershen/Desktop/linARG/data/1kg/CCDG_14151_B01_GRM_WGS_2020-08-05_chrX.filtered.eagle2-phased.v2.vcf.gz" \
    --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/chrx/" \
    --region "chrX-2781480-3781480" \
    --partition_number 0 \
    --phased \
    --flip_minor_alleles \
    --maf_filter 0.1 \
    --sex_path /Users/ambershen/Desktop/linARG/dx_analysis/chrX_testing/1kg_sex.txt \

kodama run-forward-backward --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/chrx/" --partition_identifier 0_chrX-2781480-3781480

kodama reduction-union-recom --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/chrx/" --partition_identifier 0_chrX-2781480-3781480

kodama merge --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/chrx/"

kodama add-individual-nodes --linarg_dir "/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/chrx/"
