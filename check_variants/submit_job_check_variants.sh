dx run app-swiss-army-knife \
    -iin="/amber/scripts/check_variants.py" \
    -iin="/amber/scripts/run_check_variants.sh" \
    -icmd="bash run_check_variants.sh" \
    --destination "/" \
    --instance-type "mem1_ssd1_v2_x4" \
    --priority high \
    --name "check variants" \
    --brief \
    -y