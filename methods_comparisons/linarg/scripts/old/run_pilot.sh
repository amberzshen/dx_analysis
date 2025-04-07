vcf_path="/Users/ambershen/Desktop/linARG/data/pilot_data/chr21-21990355-23324211.vcf.gz"
output_dir="/Users/ambershen/Desktop/linARG/methods_comparisons/linarg/linear_args/"

kodama make-geno \
    --vcf_path $vcf_path \
    --linarg_dir $output_dir \
    --region "chr21-21990355-23324211" \
    --partition_number 0 \
    --phased \
    --flip_minor_alleles \

kodama infer-brick-graph --linarg_dir $output_dir --partition_identifier 0_chr21-21990355-23324211

kodama merge --linarg_dir $output_dir


