#!/bin/bash
instance_type=$1

load_dir='/mnt/project/'
out_dir="amber/test_filtering"
partition_identifier="0_chr21-27946667-28988304"

for condition in "${conditions[@]}"; do


conditions = ("indel" )

linarg_dir="${out_dir}/indel/"
echo $linarg_dir
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_forward_backward_std.sh" \
    -icmd="bash run_forward_backward_std.sh $linarg_dir $load_dir $partition_identifier" \
    --destination "/" \
    --instance-type $instance_type \
    --priority low \
    --name "forward_backward_${partition_identifier}" \
    --brief \
    -y

linarg_dir="${out_dir}/maf_indel/"
echo $linarg_dir
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_forward_backward_std.sh" \
    -icmd="bash run_forward_backward_std.sh $linarg_dir $load_dir $partition_identifier" \
    --destination "/" \
    --instance-type $instance_type \
    --priority low \
    --name "forward_backward_${partition_identifier}" \
    --brief \
    -y

linarg_dir="${out_dir}/maf/"
echo $linarg_dir
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_forward_backward_std.sh" \
    -icmd="bash run_forward_backward_std.sh $linarg_dir $load_dir $partition_identifier" \
    --destination "/" \
    --instance-type $instance_type \
    --priority low \
    --name "forward_backward_${partition_identifier}" \
    --brief \
    -y


linarg_dir="${out_dir}/nofilt/"
echo $linarg_dir
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_forward_backward.sh" \
    -icmd="bash run_forward_backward.sh $linarg_dir $load_dir $partition_identifier" \
    --destination "/" \
    --instance-type $instance_type \
    --priority low \
    --name "forward_backward_nofilt_${partition_identifier}" \
    --brief \
    -y