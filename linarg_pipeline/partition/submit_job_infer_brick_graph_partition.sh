#!/bin/bash
data_identifier=$1
instance_type=$2

file_list=($(dx ls "/linear_arg_results/${data_identifier}/genotype_matrices/"))
for f in "${file_list[@]}"
do
    echo $f
    partition_identifier=$(echo "$f" | awk -F. '{print $1}')
    dx run app-swiss-army-knife \
        -iin="/amber/scripts/run_infer_brick_graph_partition.sh" \
        -iin="amber/scripts/infer_brick_graph_partition.py" \
        -iin="/linear_arg_results/${data_identifier}/genotype_matrices/${f}" \
        -icmd="bash run_infer_brick_graph_partition.sh $partition_identifier" \
        --destination "/linear_arg_results/${data_identifier}/" \
        --instance-type $instance_type \
        --priority low \
        --name "brick_graph_${data_identifier}_${partition_identifier}" \
        --brief \
        -y
done
