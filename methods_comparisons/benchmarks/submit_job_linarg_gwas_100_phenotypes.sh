# dx run app-swiss-army-knife \
#     -iin="/amber/scripts/linarg_gwas_100_phenotypes.py" \
#     -iin="/amber/scripts/run_linarg_gwas_100_phenotypes.sh" \
#     -icmd="bash run_linarg_gwas_100_phenotypes.sh 21" \
#     --destination "/amber/methods_comparisons/results/" \
#     --instance-type "mem3_ssd1_v2_x8" \
#     --priority high \
#     --name "linarg_gwas_21_100_phenotypes" \
#     --brief \
#     --ignore-reuse \
#     -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/linarg_gwas_100_phenotypes.py" \
    -iin="/amber/scripts/run_linarg_gwas_100_phenotypes.sh" \
    -icmd="bash run_linarg_gwas_100_phenotypes.sh 11" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "linarg_gwas_21_100_phenotypes" \
    --brief \
    --ignore-reuse \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/linarg_gwas_100_phenotypes.py" \
    -iin="/amber/scripts/run_linarg_gwas_100_phenotypes.sh" \
    -icmd="bash run_linarg_gwas_100_phenotypes.sh 1" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "linarg_gwas_21_100_phenotypes" \
    --brief \
    --ignore-reuse \
    -y
