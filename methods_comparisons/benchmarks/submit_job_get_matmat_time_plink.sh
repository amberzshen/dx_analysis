dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_matmat_time_plink.sh" \
    -icmd="bash get_matmat_time_plink.sh 21" \
    --destination "//amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x4" \
    --priority high \
    --name "matmat_time_plink" \
    --brief \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_matmat_time_plink.sh" \
    -icmd="bash get_matmat_time_plink.sh 11" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x4" \
    --priority high \
    --name "matmat_time_plink" \
    --brief \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_matmat_time_plink.sh" \
    -icmd="bash get_matmat_time_plink.sh 1" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd1_v2_x4" \
    --priority high \
    --name "matmat_time_plink" \
    --brief \
    -y