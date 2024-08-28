#!/bin/bash
run_identifier=$1
instance_type=$2

chrom=$(echo "$run_identifier" | awk -F_ '{print $2}' | awk -F- '{print $1}')

# dx cat "/linear_arg_results/${run_identifier}/partitions.txt > partitions.txt"
IFS=$'\n' read -r -d '' -a partitions < <(awk '{print $0}' partitions.txt)

for partition in "${partitions[@]:1}"
    do
      p=($partition)

      partition_region="$chrom-${p[1]}-${p[2]}"
      echo $partition_region

      dx run app-swiss-army-knife \
          -iin="/amber/scripts/run_get_mat_partition.sh" \
          -iin="amber/scripts/get_mat_partition.py" \
          -icmd="bash run_get_mat_partition.sh $partition_region ${p[0]}" \
          --destination "/linear_arg_results/${run_identifier}/" \
          --instance-type $instance_type \
          --priority low \
          --name "get_mat_${run_identifier}_${p[0]}_${partition_region}" \
          -y


    done


# rm partitions.txt