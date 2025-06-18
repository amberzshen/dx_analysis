dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_dp_time_plink1.9.sh" \
    -icmd="bash get_dp_time_plink1.9.sh 21" \
    --destination "/amber/methods_comparisons/results/" \
    --instance-type "mem3_ssd3_x8" \
    --priority high \
    --name "plink1.9_dp_21" \
    --brief \
    --ignore-reuse \
    -y

# dx run app-swiss-army-knife \
#     -iin="/amber/scripts/get_dp_time_plink1.9.sh" \
#     -icmd="bash get_dp_time_plink1.9.sh 11" \
#     --destination "/amber/methods_comparisons/results/" \
#     --instance-type "mem2_ssd2_v2_x32" \
#     --priority high \
#     --name "plink1.9_dp_11_short" \
#     --brief \
#     --ignore-reuse \
#     -y

# dx run app-swiss-army-knife \
#     -iin="/amber/scripts/get_dp_time_plink1.9.sh" \
#     -icmd="bash get_dp_time_plink1.9.sh 1" \
#     --destination "/amber/methods_comparisons/results/" \
#     --instance-type "mem2_ssd2_v2_x64" \
#     --priority high \
#     --name "plink1.9_dp_1_short" \
#     --brief \
#     --ignore-reuse \
#     -y