#!/bin/bash
region=$1
out_prefix=$2
partition_size=$3

chr=$(echo "$region" | awk -F: '{print $1}')
r=$(echo "$region" | awk -F: '{print $2}')
start=$(echo "$r" | awk -F- '{print $1}')
end=$(echo "$r" | awk -F- '{print $2}')

# dx mkdir -p "/genotype_matrices/${out_prefix}_${chr}\:${r}/"

# convert to integers
integer=$((start))
integer=$((end))

n_partitions=$(echo "scale=0; (($end - $start + 1) + $parition_size - 1) / $partition_size" | bc) # region is inclusive

for i in $(seq 0 $n_partitions); do
  partition_start=$(($start + i*$partition_size))
  partition_end=$(printf "%d\n%d" $(($partition_start + $partition_size - 1)) $end | sort -n | head -n1) # region is inclusive
  partition_region="$chr:$partition_start-$partition_end"
  echo $partition_region

  # dx run app-swiss-army-knife \
  #     -iin="/amber/scripts/get_genotype_mat/run_get_mat_partition.sh" \
  #     -iin="amber/scripts/get_genotype_mat/get_mat_partition.py" \
  #     -icmd="bash run_get_mat_partition.sh $partition_region $out_prefix" \
  #     --destination "/genotype_matrices/${out_prefix}_${chr}\:${r}/" \
  #     --instance-type "mem1_ssd1_v2_x4" \
  #     --priority low \
  #     --name get_mat_test \
  #     -y
done