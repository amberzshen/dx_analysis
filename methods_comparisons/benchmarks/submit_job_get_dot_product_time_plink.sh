dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time_plink.sh" \
    -icmd="bash get_dot_product_time_plink.sh 21" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "plink_dp_21_short" \
    --brief \
    --ignore-reuse \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time_plink.sh" \
    -icmd="bash get_dot_product_time_plink.sh 11" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "plink_dp_11_short" \
    --brief \
    --ignore-reuse \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time_plink.sh" \
    -icmd="bash get_dot_product_time_plink.sh 1" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "plink_dp_1_short" \
    --brief \
    --ignore-reuse \
    -y
