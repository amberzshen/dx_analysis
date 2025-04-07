dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_xsi.sh" \
    -icmd="bash run_xsi.sh" \
    --destination "/methods_comparisons/xsi/" \
    --instance-type mem3_ssd1_v2_x2 \
    --priority high \
    --name "xsi" \
    --brief \
    -y