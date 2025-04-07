# 72 cores, 144GB memory
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_grg_test.sh" \
    -iin="/methods_comparisons/grg/test-200-samples.vcf.gz" \
    -icmd="bash run_grg_test.sh" \
    --destination "/methods_comparisons/grg/" \
    --instance-type mem3_ssd1_v2_x8 \
    --priority high \
    --name "grg_test" \
    --brief \
    -y
