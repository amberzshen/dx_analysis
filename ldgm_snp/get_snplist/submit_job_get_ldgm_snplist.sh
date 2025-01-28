#!/bin/bash
instance_type="mem2_hdd2_v2_x2" # 32GB
dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_ldgm_snplist.sh" \
    -icmd="bash get_ldgm_snplist.sh" \
    --destination "/" \
    --instance-type $instance_type \
    --priority low \
    --name "get_ldgm_snplist" \
    -y
