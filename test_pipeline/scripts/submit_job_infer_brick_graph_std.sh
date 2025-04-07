#!/bin/bash
instance_type=$1

load_dir='/mnt/project/'
linarg_dir="amber/test_save_to_disk/no_save/"
partition_identifier="2_chr21-27946667-28988304"

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_infer_brick_graph_std.sh" \
    -icmd="bash run_infer_brick_graph_std.sh $linarg_dir $load_dir $partition_identifier" \
    --destination "/" \
    --instance-type $instance_type \
    --priority low \
    --name "brick_graph_${partition_identifier}" \
    --brief \
    -y