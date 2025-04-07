dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_vcf_variants.sh" \
    -icmd="bash get_vcf_variants.sh" \
    --destination "/" \
    --instance-type "mem1_ssd1_v2_x4" \
    --priority high \
    --name "count_vcf_variants" \
    --brief \
    -y