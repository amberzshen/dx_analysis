#!/bin/bash
instance_type=$1

region=""
out="linear_args"
data_identifier="ukb20279_ldgm_snplist"
chrom=1
linarg_dir="${out}/${data_identifier}/chr${chrom}/0_chr1-15916-22645888/"


vcf_path="/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c${chrom}_b0_v1.vcf.gz"

mtx_list=($(dx ls "${linarg_dir}/genotype_matrices/"))

dx download -f "/linear_args/ukb20279/chr1/0_chr1-15916-22645888/partitions.txt" # hard code
IFS=$'\n' read -r -d '' -a partitions < <(awk '{print $0}' partitions.txt)
for partition in "${partitions[@]:1}"
    do
        p=($partition)
        partition_region="${p[0]}-${p[2]}-${p[3]}"
        partition_number=${p[1]}

        if [[ " ${mtx_list[@]} " =~ " ${partition_number}_${partition_region}.npz " ]]; then # skip partitions that have already been inferred
            echo "${partition_number}_${partition_region}.npz already exists."
            continue
        fi

        echo $partition_region
        dx run app-swiss-army-knife \
            -iin="/amber/scripts/run_get_geno_filter.sh" \
            -iin="/amber/scripts/get_geno_filter.py" \
            -icmd="bash run_get_geno_filter.sh \"$vcf_path\" $linarg_dir $partition_region $partition_number" \
            --destination "/" \
            --instance-type $instance_type \
            --priority low \
            --name "get_mat_${partition_region}" \
            --brief \
            -y
    done

rm partitions.txt