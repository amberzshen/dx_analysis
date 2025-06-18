dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_ukb_maf_0.01_stats.py" \
    -iin="/amber/scripts/run_get_ukb_maf_0.01_stats.sh" \
    -icmd="bash run_get_ukb_maf_0.01_stats.sh" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x2" \
    --priority high \
    --name "ukb_maf_0.01_stats" \
    --brief \
    -y