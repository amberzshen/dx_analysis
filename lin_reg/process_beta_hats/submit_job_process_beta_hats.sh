#!/bin/bash
linarg_dir="/mnt/project/linear_args/ukb20279/chr1/"
beta_dir="/mnt/project/lin_reg_benchmark/whitelist_sanity_check_chr22/beta_hats/"
out_dir="lin_reg_benchmark/whitelist_sanity_check_chr22/"

partition_ids=( $(dx ls linear_args/ukb20279/chr1/) )
for partition_id in "${partition_ids[@]}"
    do
        partition_id=$(echo "$partition_id" | rev | cut -c 2- | rev)
        echo $partition_id

        instance_type="mem3_hdd2_v2_x2" # 16GB
        dx run app-swiss-army-knife \
            -iin="/amber/scripts/run_process_beta_hats.sh" \
            -iin="/amber/scripts/process_beta_hats.py" \
            -icmd="bash run_process_beta_hats.sh $linarg_dir $beta_dir $partition_id $out_dir" \
            --destination "/" \
            --instance-type $instance_type \
            --priority low \
            --name "process_beta_hats" \
            --brief \
            -y
        
        break
    done