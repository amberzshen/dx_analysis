chrom=$1

vcf_path="/mnt/project/amber/filtered_vcfs/ukb20279_c${chrom}_b0_v1_250129_whitelist.vcf.gz"
output_prefix="ukb20279_c${chrom}_b0_v1_250129_whitelist"

plink2 --vcf $vcf_path --make-bed --out output_prefix
