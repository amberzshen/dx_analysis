#!/bin/bash
instance_type="mem3_ssd1_v2_x4" # 32GB
out="linear_args"
data_identifier="ukb20279"
chroms=({1..22})

for chrom in "${chroms[@]}"; do

    # test run
    # if [[ $chrom != 21 ]]; then
    #     continue 
    # fi

    chrom_dir="${out}/${data_identifier}/chr${chrom}"
    linarg_dir_list=($(dx ls $chrom_dir))

    for dir in ${linarg_dir_list[@]}; do
        linarg_dir=${chrom_dir}/${dir}
        output_list=($(dx ls "${linarg_dir}"))
        if [[ " ${output_list[@]} " =~ " linear_arg.h5 " ]]; then # skip partitions that have already been inferred
                echo "${linarg_dir} has already been converted."
                continue
        fi

        echo $linarg_dir

        dx run app-swiss-army-knife \
            -iin="/amber/scripts/change_file_format.py" \
            -iin="/amber/scripts/run_change_file_format.sh" \
            -icmd="bash run_change_file_format.sh $linarg_dir" \
            --destination "/" \
            --instance-type $instance_type \
            --priority low \
            --name "convert_${linarg_dir}" \
            --brief \
            -y
    done
done