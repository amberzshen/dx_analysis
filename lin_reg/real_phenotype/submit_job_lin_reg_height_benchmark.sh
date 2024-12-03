#!/bin/bash

linarg_dir="/mnt/project/linear_args/ukb20279/chr1/"
linarg_dx_dir="linear_args/ukb20279/chr1/"
res_dir="lin_reg_benchmark/height_benchmark_scipy1.14.1"

# partition_id="0_chr1-15916-22645888"
# data_type="linarg"
# instance_type="mem1_ssd1_v2_x8" # 16GB
# dx run app-swiss-army-knife \
#     -iin="/amber/scripts/run_lin_reg_height_benchmark.sh" \
#     -iin="/amber/scripts/lin_reg_height_benchmark.py" \
#     -icmd="bash run_lin_reg_height_benchmark.sh $linarg_dir $partition_id $data_type $res_dir" \
#     --destination "/" \
#     --instance-type $instance_type \
#     --priority low \
#     --name "lin_reg_height_benchmark_${partition_id}" \
#     --brief \
#     -y

# data_type="genotypes"
# instance_type="mem3_ssd1_v2_x16" # 128GB
# dx run app-swiss-army-knife \
#     -iin="/amber/scripts/run_lin_reg_height_benchmark.sh" \
#     -iin="/amber/scripts/lin_reg_height_benchmark.py" \
#     -icmd="bash run_lin_reg_height_benchmark.sh $linarg_dir $partition_id $data_type $res_dir" \
#     --destination "/" \
#     --instance-type $instance_type \
#     --priority low \
#     --name "lin_reg_height_benchmark_${partition_id}" \
#     --brief \
#     -y

partition_ids=( $(dx ls linear_args/ukb20279/chr1/) )

for partition_id in "${partition_ids[@]:1}"
    do
        partition_id=$(echo "$partition_id" | rev | cut -c 2- | rev)
        echo $partition_id

        data_type="linarg"
        instance_type="mem1_ssd1_v2_x8" # 16GB
        dx run app-swiss-army-knife \
            -iin="/amber/scripts/run_lin_reg_height_benchmark.sh" \
            -iin="/amber/scripts/lin_reg_height_benchmark.py" \
            -icmd="bash run_lin_reg_height_benchmark.sh $linarg_dir $partition_id $data_type $res_dir" \
            --destination "/" \
            --instance-type $instance_type \
            --priority low \
            --name "lin_reg_height_benchmark_${partition_id}" \
            --brief \
            -y

        data_type="genotypes"
        instance_type="mem3_ssd1_v2_x16" # 128GB
        dx run app-swiss-army-knife \
            -iin="/amber/scripts/run_lin_reg_height_benchmark.sh" \
            -iin="/amber/scripts/lin_reg_height_benchmark.py" \
            -icmd="bash run_lin_reg_height_benchmark.sh $linarg_dir $partition_id $data_type $res_dir" \
            --destination "/" \
            --instance-type $instance_type \
            --priority low \
            --name "lin_reg_height_benchmark_${partition_id}" \
            --brief \
            -y
    done

