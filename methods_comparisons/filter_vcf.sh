chr=$1

whitelist_path="/mnt/project/sample_metadata/ukb20279/250129_whitelist.txt"
vcf_path="/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c${chr}_b0_v1.vcf.gz"
out="amber/filtered_vcfs/ukb20279_c${chr}_b0_v1_250129_whitelist.vcf.gz"

mkdir -p amber/filtered_vcfs
bcftools view -S "$whitelist_path" -Oz -o "$out" "$vcf_path"
bcftools index "$out"
