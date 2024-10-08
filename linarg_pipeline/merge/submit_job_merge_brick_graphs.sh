#!/bin/bash
run_identifier=$1
instance_type=$2

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_merge_brick_graphs.sh" \
    -iin="amber/scripts/merge_brick_graphs.py" \
    -icmd="bash run_merge_brick_graphs.sh $run_identifier" \
    --destination "/linear_arg_results/" \
    --instance-type $instance_type \
    --priority low \
    --name "linarg_merge_${run_identifier}_${partition_identifier}" \
    --brief \
    -y
