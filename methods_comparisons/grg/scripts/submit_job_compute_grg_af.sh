dx run app-swiss-army-knife \
    -iin="/amber/scripts/compute_grg_af.sh" \
    -iin="/methods_comparisons/grg/ukb20279_c21_b0_v1_250129_whitelist.grg" \
    -icmd="bash compute_grg_af.sh" \
    --destination "/methods_comparisons/grg/" \
    --instance-type mem3_ssd1_v2_x16  \
    --priority high \
    --name "grg_af" \
    --brief \
    -y
