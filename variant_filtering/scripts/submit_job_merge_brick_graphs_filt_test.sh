#!/bin/bash
instance_type="mem3_ssd1_v2_x8" # 64GB

load_dir='/mnt/project/'
out_dir="amber/test_filtering"

# conditions = ("indel" "maf_indel" "maf" "nofilt")

for condition in indel maf_indel maf nofilt; do

    linarg_dir="${out_dir}/${condition}/"
    echo $linarg_dir
    dx run app-swiss-army-knife \
        -iin="/amber/scripts/run_merge_brick_graphs.sh" \
        -icmd="bash run_merge_brick_graphs.sh $linarg_dir $load_dir" \
        --destination "/" \
        --instance-type $instance_type \
        --priority high \
        --name "reduction_union_recom_${condition}_${partition_identifier}" \
        --brief \
        -y
done