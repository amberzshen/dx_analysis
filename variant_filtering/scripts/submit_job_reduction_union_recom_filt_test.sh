#!/bin/bash
instance_type="mem3_ssd1_v2_x32" # 256GB

load_dir='/mnt/project/'
out_dir="amber/test_filtering"
partition_identifier="0_chr21-27946667-28988304"

# conditions = ( "indel" "maf_indel" "maf" "nofilt" )

for condition in indel maf_indel maf nofilt; do

    linarg_dir="${out_dir}/${condition}/"
    echo $linarg_dir
    dx run app-swiss-army-knife \
        -iin="/amber/scripts/run_reduction_union_recom.sh" \
        -icmd="bash run_reduction_union_recom.sh $linarg_dir $load_dir $partition_identifier" \
        --destination "/" \
        --instance-type $instance_type \
        --priority high \
        --name "reduction_union_recom_${condition}_${partition_identifier}" \
        --brief \
        -y
done