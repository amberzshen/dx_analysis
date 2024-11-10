#!/bin/bash

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_get_vcf_region.sh" \
    -iin="/amber/scripts/get_vcf_region.py" \
    -icmd="bash run_get_vcf_region.sh" \
    --destination "/" \
    --instance-type mem1_ssd1_v2_x4 \
    --priority high \
    --name "get_vcf_region" \
    -y