#!/bin/bash
region=$1 # should be in the form: chrA-B-C
out_prefix=$2
window_size=$3
instance_type=$4

dx mkdir -p "/linear_arg_results/${out_prefix}_${region}/"

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_get_partitions.sh" \
    -iin="amber/scripts/get_partitions.py" \
    -icmd="bash run_get_partitions.sh $region $window_size" \
    --destination "/linear_arg_results/${out_prefix}_${region}/" \
    --instance-type $instance_type \
    --priority high \
    --name "get_partition_${out_prefix}_${region}" \
    -y
