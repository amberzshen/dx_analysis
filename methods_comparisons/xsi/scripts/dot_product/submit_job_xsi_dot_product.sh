dx run app-swiss-army-knife \
    -iin="/amber/scripts/xsi_dot_product.sh" \
    -icmd="bash xsi_dot_product.sh" \
    --destination "/methods_comparisons/xsi/" \
    --instance-type mem3_ssd1_v2_x2 \
    --priority high \
    --name "xsi_dot_product" \
    --brief \
    -y