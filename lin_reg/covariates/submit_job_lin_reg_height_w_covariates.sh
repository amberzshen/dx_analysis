#!/bin/bash

linarg_dir="/mnt/project/linear_args/ukb20279/chr1/"
linarg_dx_dir="linear_args/ukb20279/chr1/"
res_dir="lin_reg_benchmark/height_benchmark_w_covariates_Ynorm"

# partition_id="0_chr1-15916-22645888"
# data_type="linarg"
# instance_type="mem3_ssd1_v2_x4" # 32GB
# dx run app-swiss-army-knife \
#     -iin="/amber/scripts/run_lin_reg_height_w_covariates.sh" \
#     -iin="/amber/scripts/lin_reg_height_w_covariates.py" \
#     -icmd="bash run_lin_reg_height_w_covariates.sh $linarg_dir $partition_id $data_type $res_dir" \
#     --destination "/" \
#     --instance-type $instance_type \
#     --priority low \
#     --name "lin_reg_height_w_covariates_${data_type}_${partition_id}" \
#     --brief \
#     -y

# data_type="genotypes"
# instance_type="mem2_ssd1_v2_x64" # 256GB
# dx run app-swiss-army-knife \
#     -iin="/amber/scripts/run_lin_reg_height_w_covariates.sh" \
#     -iin="/amber/scripts/lin_reg_height_w_covariates.py" \
#     -icmd="bash run_lin_reg_height_w_covariates.sh $linarg_dir $partition_id $data_type $res_dir" \
#     --destination "/" \
#     --instance-type $instance_type \
#     --priority low \
#     --name "lin_reg_height_w_covariates_${data_type}_${partition_id}" \
#     --brief \
#     -y


partition_ids=( $(dx ls linear_args/ukb20279/chr1/) )
for partition_id in "${partition_ids[@]}"
    do
        partition_id=$(echo "$partition_id" | rev | cut -c 2- | rev)
        echo $partition_id

        data_type="linarg"
        instance_type="mem3_ssd1_v2_x4" # 32GB
        dx run app-swiss-army-knife \
            -iin="/amber/scripts/run_lin_reg_height_w_covariates.sh" \
            -iin="/amber/scripts/lin_reg_height_w_covariates.py" \
            -icmd="bash run_lin_reg_height_w_covariates.sh $linarg_dir $partition_id $data_type $res_dir" \
            --destination "/" \
            --instance-type $instance_type \
            --priority low \
            --name "lin_reg_height_w_covariates_${data_type}_${partition_id}" \
            --brief \
            -y

        data_type="genotypes"
        instance_type="mem2_ssd1_v2_x64" # 256GB
        dx run app-swiss-army-knife \
            -iin="/amber/scripts/run_lin_reg_height_w_covariates.sh" \
            -iin="/amber/scripts/lin_reg_height_w_covariates.py" \
            -icmd="bash run_lin_reg_height_w_covariates.sh $linarg_dir $partition_id $data_type $res_dir" \
            --destination "/" \
            --instance-type $instance_type \
            --priority low \
            --name "lin_reg_height_w_covariates_${data_type}_${partition_id}" \
            --brief \
            -y

    done

