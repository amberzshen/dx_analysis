dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dot_product_time.py" \
    -iin="/amber/scripts/run_get_dot_product_time.sh" \
    -icmd="bash run_get_dot_product_time.sh" \
    --destination "/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "dot_product_time" \
    --brief \
    -y