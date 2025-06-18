chrom=$1

vcf_path="/mnt/project/amber/filtered_vcfs"
bcftools view -i 'MAF>=0.01' "$vcf_path" -Oz -o ukb20279_c${chrom}_b0_v1_maf_0.01.vcf.gz
