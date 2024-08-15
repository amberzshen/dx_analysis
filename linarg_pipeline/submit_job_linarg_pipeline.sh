#!/bin/bash
data_identifier=$1

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_linarg_pipeline.sh" \
    -iin="amber/scripts/linarg_pipeline.py" \
    -inn="/genotype_matrices/matrices/${data_identifier}.npz" \
    -inn="/genotype_matrices/variant_metadata/${data_identifier}.txt" \
    -icmd="bash run_linarg_pipeline.sh $data_indentifier" \
    --destination "/" \
    --instance-type "mem1_ssd1_v2_x4" \
    --priority low \
    --name run_linarg_pipeline_test \
    -y
