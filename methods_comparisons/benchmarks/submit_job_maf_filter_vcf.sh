dx run app-swiss-army-knife \
    -iin="/amber/scripts/maf_filter_vcf.sh" \
    -icmd="bash maf_filter_vcf.sh 1" \
    --destination "amber/filtered_vcfs/" \
    --instance-type "mem3_ssd1_v2_x2" \
    --priority high \
    --name "maf_filter_vcf" \
    --brief \
    -y