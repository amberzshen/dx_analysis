#!/bin/bash
instance_type="mem3_ssd1_v2_x2" # 16GB

vcf_path="/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c21_b0_v1.vcf.gz"
out_dir="amber/test_filtering"
partition_region="chr21-27946667-28988304"
whitelist_path="/mnt/project/sample_metadata/ukb20279/250129_whitelist.txt"


linarg_dir="${out_dir}/indel/"
echo $linarg_dir
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_get_geno_partition_indel.sh" \
    -icmd="bash run_get_geno_partition_indel.sh \"$vcf_path\" $linarg_dir $partition_region $whitelist_path" \
    --destination "/" \
    --instance-type $instance_type \
    --priority high \
    --name "get_mat_indel_${partition_region}" \
    --brief \
    -y


linarg_dir="${out_dir}/maf_indel/"
echo $linarg_dir
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_get_geno_partition_maf_indel.sh" \
    -icmd="bash run_get_geno_partition_maf_indel.sh \"$vcf_path\" $linarg_dir $partition_region $whitelist_path" \
    --destination "/" \
    --instance-type $instance_type \
    --priority high \
    --name "get_mat_maf_indel_${partition_region}" \
    --brief \
    -y


linarg_dir="${out_dir}/maf/"
echo $linarg_dir
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_get_geno_partition_maf.sh" \
    -icmd="bash run_get_geno_partition_maf.sh \"$vcf_path\" $linarg_dir $partition_region $whitelist_path" \
    --destination "/" \
    --instance-type $instance_type \
    --priority high \
    --name "get_mat_maf_${partition_region}" \
    --brief \
    -y


linarg_dir="${out_dir}/nofilt/"
echo $linarg_dir
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_get_geno_partition_nofilt.sh" \
    -icmd="bash run_get_geno_partition_nofilt.sh \"$vcf_path\" $linarg_dir $partition_region $whitelist_path" \
    --destination "/" \
    --instance-type $instance_type \
    --priority high \
    --name "get_mat_nofilt_${partition_region}" \
    --brief \
    -y

