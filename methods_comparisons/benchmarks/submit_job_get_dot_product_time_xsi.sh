dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time_xsi.sh" \
    -iin="/amber/scripts/profile.sh" \
    -icmd="bash get_dot_product_time_xsi.sh 21" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "dot_product_time_21" \
    --brief \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time_xsi.sh" \
    -iin="/amber/scripts/profile.sh" \
    -icmd="bash get_dot_product_time_xsi.sh 11" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "dot_product_time_11" \
    --brief \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time_xsi.sh" \
    -iin="/amber/scripts/profile.sh" \
    -icmd="bash get_dot_product_time_xsi.sh 1" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "dot_product_time_1" \
    --brief \
    -y