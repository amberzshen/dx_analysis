dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_gwas_time_grg.sh" \
    -icmd="bash get_gwas_time_grg.sh 21" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "grg_gwas_21_short" \
    --brief \
    --ignore-reuse \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_gwas_time_grg.sh" \
    -icmd="bash get_gwas_time_grg.sh 11" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "grg_gwas_11_short" \
    --brief \
    --ignore-reuse \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_gwas_time_grg.sh" \
    -icmd="bash get_gwas_time_grg.sh 1" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "grg_gwas_1_short" \
    --brief \
    --ignore-reuse \
    -y