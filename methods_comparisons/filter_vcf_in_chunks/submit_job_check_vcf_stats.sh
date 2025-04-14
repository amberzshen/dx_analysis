vcf_file="/mnt/project/amber/filtered_vcfs/ukb20279_c1_b0_v1_250129_whitelist.vcf.gz"

dx run app-swiss-army-knife \
    -iin="/amber/scripts/check_vcf_stats.sh" \
    -icmd="bash check_vcf_stats.sh $vcf_file" \
    --destination "/" \
    --instance-type mem1_ssd1_v2_x2 \
    --priority high \
    --name "get_filtered_vcf_stats" \
    --brief \
    -y
