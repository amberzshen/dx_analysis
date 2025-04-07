dx run app-swiss-army-knife \
    -iin="/amber/scripts/convert_to_igd.sh" \
    -icmd="bash convert_to_igd.sh" \
    --destination "/methods_comparisons/grg/" \
    --instance-type mem3_ssd1_v2_x2 \
    --priority high \
    --name "grg" \
    --brief \
    -y
