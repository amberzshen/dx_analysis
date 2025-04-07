#!/bin/bash
instance_type=$1

vcf_path="/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c21_b0_v1.vcf.gz"
out_dir="amber/test_save_to_disk/"
partition_region="chr21-27946667-28988304"
whitelist_path="/mnt/project/sample_metadata/ukb20279/250129_whitelist.txt"

conditions=("save" "no_save")

for condition in "${conditions[@]}"; do

    linarg_dir="${out_dir}${condition}"
    echo $linarg_dir
    dx run app-swiss-army-knife \
        -iin="/amber/scripts/run_get_geno_partition_std.sh" \
        -icmd="bash run_get_geno_partition_std.sh \"$vcf_path\" $linarg_dir $partition_region $whitelist_path" \
        --destination "/" \
        --instance-type $instance_type \
        --priority low \
        --name "get_mat_${partition_region}" \
        --brief \
        -y
done


