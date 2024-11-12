#!/bin/bash

linarg_dir="/mnt/project/linear_args/ukb20279/chr1/0_chr1-15916-22645888"
linarg_dx_dir="linear_args/ukb20279/chr1/0_chr1-15916-22645888"
res_dir="lin_reg_benchmark"
instance_type="mem1_ssd1_v2_x4"

dx download -f "${linarg_dx_dir}/partitions.txt"
IFS=$'\n' read -r -d '' -a partitions < <(awk '{print $0}' partitions.txt)

data_type="linarg"
for partition in "${partitions[@]:1}"
    do
        p=($partition)
        partition_id="${p[1]}_${p[0]}-${p[2]}-${p[3]}"

        echo $partition_id
        dx run app-swiss-army-knife \
            -iin="/amber/scripts/run_lin_reg_benchmark.sh" \
            -iin="/amber/scripts/lin_reg_benchmark.py" \
            -icmd="bash run_lin_reg_benchmark.sh $linarg_dir $partition_id $data_type $res_dir" \
            --destination "/" \
            --instance-type $instance_type \
            --priority low \
            --name "lin_reg_benchmark_${partition_id}" \
            --brief \
            -y
    done

data_type="genotypes"
for partition in "${partitions[@]:1}"
    do
        p=($partition)
        partition_id="${p[1]}_${p[0]}-${p[2]}-${p[3]}"

        echo $partition_id
        dx run app-swiss-army-knife \
            -iin="/amber/scripts/run_lin_reg_benchmark.sh" \
            -iin="/amber/scripts/lin_reg_benchmark.py" \
            -icmd="bash run_lin_reg_benchmark.sh $linarg_dir $partition_id $data_type $res_dir" \
            --destination "/" \
            --instance-type $instance_type \
            --priority low \
            --name "lin_reg_benchmark_${partition_id}" \
            --brief \
            -y
    done

rm partitions.txt