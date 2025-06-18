dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_gwas_dp_time_plink_nocovar.sh" \
    -icmd="bash get_gwas_dp_time_plink_nocovar.sh" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x32" \
    --priority high \
    --name "plink_gwas_21_nocovar" \
    --brief \
    --ignore-reuse \
    -y