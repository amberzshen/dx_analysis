dx run app-swiss-army-knife \
    -iin="/amber/scripts/test_hwe.sh" \
    -icmd="bash test_hwe.sh" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x2" \
    --priority high \
    --name "hwe" \
    --brief \
    --ignore-reuse \
    -y

