dx run app-swiss-army-knife \
    -iin="/amber/scripts/download_test.sh" \
    -iin="/methods_comparisons/grg/test-200-samples.vcf.gz" \
    -icmd="bash download_test.sh" \
    --destination "/methods_comparisons/grg/" \
    --instance-type mem1_ssd1_v2_x2  \
    --priority high \
    --name "download_grg_test" \
    --brief \
    -y
