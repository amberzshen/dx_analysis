dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_gwas_time_plink.sh" \
    -icmd="bash get_gwas_time_plink.sh 21" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "plink_gwas_21_short" \
    --brief \
    --ignore-reuse \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_gwas_time_plink.sh" \
    -icmd="bash get_gwas_time_plink.sh 11" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "plink_gwas_11_short" \
    --brief \
    --ignore-reuse \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_gwas_time_plink.sh" \
    -icmd="bash get_gwas_time_plink.sh 1" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "plink_gwas_1_short" \
    --brief \
    --ignore-reuse \
    -y