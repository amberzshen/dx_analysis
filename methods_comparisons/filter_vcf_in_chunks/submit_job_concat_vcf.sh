dx run app-swiss-army-knife \
    -iin="/amber/scripts/concat_vcf.sh" \
    -icmd="bash concat_vcf.sh" \
    --destination "/amber/filtered_vcfs/" \
    --instance-type mem3_ssd1_v2_x8 \
    --priority high \
    --name "concat_vcf" \
    --brief \
    -y
