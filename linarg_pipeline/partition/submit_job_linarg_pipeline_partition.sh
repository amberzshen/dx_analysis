#!/bin/bash
data_identifier=$1
instance_type=$2

file_list=($(dx ls "/results/genotype_matrices/${data_identifier}"))
for partition_identifier in "${file_list[@]}"
do
    dx run app-swiss-army-knife \
        -iin="/amber/scripts/linarg_pipeline/run_linarg_pipeline_partition.sh" \
        -iin="amber/scripts/linarg_pipeline/linarg_pipeline_partition.py" \
        -iin="/linear_arg_results/genotype_matrices/${partition_identifier}.npz" \
        -icmd="bash run_linarg_pipeline.sh $partition_identifier" \
        --destination "/" \
        --instance-type $instance_type \
        --priority low \
        --name "linarg_${data_identifier}_${partition_identifier}" \
        -y
done