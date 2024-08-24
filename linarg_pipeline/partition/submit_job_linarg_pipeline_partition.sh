#!/bin/bash
data_identifier=$1
instance_type=$2

file_list=($(dx ls "/linear_arg_results/${data_identifier}/genotype_matrices/"))
for f in "${file_list[@]}"
do
    echo $f
    partition_identifier=$(echo "$f" | awk -F. '{print $1}')
    dx run app-swiss-army-knife \
        -iin="/amber/scripts/run_linarg_pipeline_partition.sh" \
        -iin="amber/scripts/linarg_pipeline_partition.py" \
        -iin="/linear_arg_results/${data_identifier}/genotype_matrices/${partition_identifier}.npz" \
        -icmd="bash run_linarg_pipeline.sh $partition_identifier" \
        --destination "/" \
        --instance-type $instance_type \
        --priority low \
        --name "linarg_${data_identifier}_${partition_identifier}" \
        -y
done
