#!/bin/bash
data_identifier=$1

echo $data_identifier

dx run app-swiss-army-knife \
    -iin="/amber/scripts/linarg_pipeline/run_linarg_pipeline.sh" \
    -iin="amber/scripts/linarg_pipeline/linarg_pipeline.py" \
    -iin="/genotype_matrices/matrices/${data_identifier}.npz" \
    -iin="/genotype_matrices/variant_metadata/${data_identifier}.txt" \
    -icmd="bash run_linarg_pipeline.sh $data_identifier" \
    --destination "/" \
    --instance-type "mem3_ssd1_v2_x2" \
    --priority low \
    --name run_linarg_pipeline_test \
    -y
