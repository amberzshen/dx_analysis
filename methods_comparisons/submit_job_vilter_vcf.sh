dx run app-swiss-army-knife \
    -iin="/amber/scripts/filter_vcf.sh" \
    -icmd="bash filter_vcf.sh 1" \
    --destination "/" \
    --instance-type mem1_ssd1_v2_x4 \
    --priority high \
    --name "filter_vcf_1" \
    --brief \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/filter_vcf.sh" \
    -icmd="bash filter_vcf.sh 11" \
    --destination "/" \
    --instance-type mem1_ssd1_v2_x4 \
    --priority high \
    --name "filter_vcf_11" \
    --brief \
    -y