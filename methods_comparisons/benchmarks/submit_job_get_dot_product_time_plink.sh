dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time_plink.sh" \
    -icmd="bash get_dot_product_time_plink.sh 21" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "plink_dp_21" \
    --brief \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time_plink.sh" \
    -icmd="bash get_dot_product_time_plink.sh 11" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "plink_dp_11" \
    --brief \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time_plink.sh" \
    -icmd="bash get_dot_product_time_plink.sh 1" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "plink_dp_1" \
    --brief \
    -y