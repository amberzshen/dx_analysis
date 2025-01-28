dx run app-swiss-army-knife \
    -icmd='bcftools query -l "/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c1_b0_v1.vcf.gz" > sample_ids.txt' \
    --destination "/sample_metadata/ukb20279/" \
    --instance-type "mem1_ssd1_v2_x4" \
    --priority low \
    --name "get_sample_ids" \
    --brief \
    -y
