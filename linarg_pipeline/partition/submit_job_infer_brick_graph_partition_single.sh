#!/bin/bash
run_identifier=$1
partition_identifier=$2
instance_type=$3

f="${partition_identifier}.npz"

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_infer_brick_graph_partition.sh" \
    -iin="amber/scripts/infer_brick_graph_partition.py" \
    -iin="/linear_arg_results/${run_identifier}/genotype_matrices/${f}" \
    -icmd="bash run_infer_brick_graph_partition.sh $partition_identifier" \
    --destination "/linear_arg_results/${run_identifier}/" \
    --instance-type $instance_type \
    --priority low \
    --name "brick_graph_${run_identifier}_${partition_identifier}" \
    --brief \
    -y