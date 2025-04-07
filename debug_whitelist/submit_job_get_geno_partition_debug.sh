#!/bin/bash
instance_type=$1

vcf_path="/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c22_b0_v1.vcf.gz"
linarg_dir="debug_whitelist"
partition_region="chr22-10521887-11029033"
whitelist_path="/mnt/project/sample_metadata/ukb20279/250129_whitelist.txt"

echo $partition_region
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_get_geno_partition_debug.sh" \
    -icmd="bash run_get_geno_partition_debug.sh \"$vcf_path\" $linarg_dir $partition_region $whitelist_path" \
    --destination "/" \
    --instance-type $instance_type \
    --priority high \
    --name "get_mat_${partition_region}" \
    --brief \
    -y
