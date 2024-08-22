#!/bin/bash
region=$1
out_prefix=$2

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_genotype_mat/run_get_mat.sh" \
    -iin="amber/scripts/get_genotype_mat/get_mat.py" \
    -icmd="bash run_get_mat.sh $region $out_prefix" \
    --destination "/" \
    --instance-type "mem3_ssd1_v2_x4" \
    --priority high \
    --name get_mat_test \
    -y