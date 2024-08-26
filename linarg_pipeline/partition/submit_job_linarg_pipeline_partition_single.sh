#!/bin/bash
data_identifier=$1
partition_identifier=$2
instance_type=$3

f="${partition_identifier}.npz"

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_linarg_pipeline_partition.sh" \
    -iin="amber/scripts/linarg_pipeline_partition.py" \
    -iin="/linear_arg_results/${data_identifier}/genotype_matrices/${f}" \
    -icmd="bash run_linarg_pipeline_partition.sh $partition_identifier" \
    --destination "/linear_arg_results/${data_identifier}/" \
    --instance-type $instance_type \
    --priority low \
    --name "linarg_${data_identifier}_${partition_identifier}" \
    --brief \
    -y