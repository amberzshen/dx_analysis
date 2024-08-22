#!/bin/bash
region=$1
out_prefix=$2
partition_size=$3

dx mkdir -p "genotype_matrices/${region}_${out_prefix}/"

chr=$(echo "$region" | awk -F: '{print $1}')
r=$(echo "$region" | awk -F: '{print $2}')
start=$(echo "$r" | awk -F- '{print $1}')
end=$(echo "$r" | awk -F- '{print $2}')

# convert to integers
integer=$((start))
integer=$((end))

n_partitions=$(echo "scale=0; (($end - $start) + $parition_size - 1) / $partition_size" | bc)

for i in $(seq 0 $n_partitions); do
  partition_start=$(($start + i*$partition_size))
  partition_end=$(printf "%d\n%d" $(($partition_start + $partition_size - 1)) $end | sort -n | head -n1) # double check that start and end are inclusive
  partition_region="$chr:$partition_start-$partition_end"
  echo $partition_region

  dx run app-swiss-army-knife \
      -iin="/amber/scripts/get_genotype_mat/run_get_mat.sh" \
      -iin="amber/scripts/get_genotype_mat/get_mat.py" \
      -icmd="bash run_get_mat.sh $partition_region $out_prefix" \
      --destination "/genotype_matrices/${region}_${out_prefix}/" \
      --instance-type "mem3_ssd1_v2_x4" \
      --priority high \
      --name get_mat_test \
      -y
done