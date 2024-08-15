#!/bin/bash
chrom=$1
region=$2
out_prefix=$3

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_get_mat.sh" \
    -iin="amber/scripts/get_mat.py" \
    -icmd="bash run_get_mat.sh $chrom $region $out_prefix" \
    --destination "/" \
    --instance-type "mem2_ssd1_v2_x4" \
    --priority low \
    --name get_mat_test \
    -y
