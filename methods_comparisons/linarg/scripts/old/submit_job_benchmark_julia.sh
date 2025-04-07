instance_type="mem3_ssd1_v2_x2" # 16GB
dx run app-swiss-army-knife \
    -iin="/amber/scripts/benchmark_julia.sh" \
    -icmd="bash benchmark_julia.sh" \
    --destination "/methods_comparisons/linarg/" \
    --instance-type $instance_type \
    --priority high \
    --name "linarg_dot_product" \
    --brief \
    -y
