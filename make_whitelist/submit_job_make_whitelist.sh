#!/bin/bash
region=$1
out_prefix=$2

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_make_whitelist.sh" \
    -iin="amber/scripts/make_whitelist.py" \
    -icmd="bash run_make_whitelist.sh" \
    --destination "/sample_metadata/ukb20279/" \
    --instance-type "mem1_ssd1_v2_x4" \
    --priority low \
    --name make_whitelist \
    -y
