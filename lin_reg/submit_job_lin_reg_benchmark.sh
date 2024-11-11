#!/bin/bash

linarg_dir="/linear_args/ukb20279/chr1/0_chr1-15916-22645888"
partition_id="0_chr1-15916-1093532"
data_type="linarg"
res_dir="lin_reg_benchmark"

instance_type="mem1_ssd1_v2_x4"

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_lin_reg_benchmark.sh" \
    -iin="/amber/scripts/lin_reg_benchmark.py" \
    -icmd="bash run_lin_reg_benchmark.sh $linarg_dir $partition_id $data_type $red_dir" \
    --destination "/" \
    --instance-type $instance_type \
    --priority low \
    --name "lin_reg_benchmark_${partition_id}" \
    --brief \
    -y