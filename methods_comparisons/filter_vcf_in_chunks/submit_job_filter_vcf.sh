# partition_path="/Users/ambershen/Desktop/linARG/dx_analysis/methods_comparisons/filter_vcf_in_chunks/partitions/chr11_partitions.txt"
partition_path="/Users/ambershen/Desktop/linARG/dx_analysis/methods_comparisons/filter_vcf_in_chunks/partitions/chr1_partitions.txt"
IFS=$'\n' read -r -d '' -a partitions < <(awk '{print $0}' $partition_path)
for partition in "${partitions[@]:1}"; do

    p=($partition)
    partition_region="chr${p[0]}:${p[2]}-${p[3]}"
    partition_number=${p[1]}
    echo ${p[0]} ${partition_region} ${partition_number}

    dx run app-swiss-army-knife \
        -iin="/amber/scripts/filter_vcf.sh" \
        -icmd="bash filter_vcf.sh ${p[0]} ${partition_region} ${partition_number}" \
        --destination "/" \
        --instance-type mem1_ssd1_v2_x2 \
        --priority high \
        --name "filter_vcf_${partition_number}" \
        --brief \
        -y
done