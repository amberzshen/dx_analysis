dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time_grg.py" \
    -iin="/amber/scripts/run_get_dot_product_time_grg.sh" \
    -icmd="bash run_get_dot_product_time_grg.sh" \
    --destination "/" \
    --instance-type "mem3_ssd1_v2_x4" \
    --priority high \
    --name "grg_dp_time" \
    --brief \
    -y