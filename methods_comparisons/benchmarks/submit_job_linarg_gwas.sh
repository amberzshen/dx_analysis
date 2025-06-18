dx run app-swiss-army-knife \
    -iin="/amber/scripts/linarg_gwas.py" \
    -iin="/amber/scripts/run_linarg_gwas.sh" \
    -icmd="bash run_linarg_gwas.sh 21" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x4" \
    --priority high \
    --name "linarg_gwas_21_short" \
    --brief \
    --ignore-reuse \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/linarg_gwas.py" \
    -iin="/amber/scripts/run_linarg_gwas.sh" \
    -icmd="bash run_linarg_gwas.sh 11" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x4" \
    --priority high \
    --name "linarg_gwas_11_short" \
    --brief \
    --ignore-reuse \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/linarg_gwas.py" \
    -iin="/amber/scripts/run_linarg_gwas.sh" \
    -icmd="bash run_linarg_gwas.sh 1" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x4" \
    --priority high \
    --name "linarg_gwas_1_short" \
    --brief \
    --ignore-reuse \
    -y