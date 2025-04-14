chr=$1
region=$2
partition_number=$3

### testing ###
# vcf_path="/Users/ambershen/Desktop/linARG/data/1kg/CCDG_14151_B01_GRM_WGS_2020-08-05_chr${chr}.filtered.shapeit2-duohmm-phased.vcf.gz"
# out="/Users/ambershen/Desktop/linARG/dx_analysis/methods_comparisons/filter_vcf_in_chunks/test/partitions/${partition_number}_${region}.vcf.gz"
# bcftools view --regions-overlap 0 --regions $region -Oz -o "$out" "$vcf_path"

whitelist_path="/mnt/project/sample_metadata/ukb20279/250129_whitelist.txt"
vcf_path="/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c${chr}_b0_v1.vcf.gz"
out="amber/filtered_vcfs/chr${chr}/${partition_number}_${region}_ukb20279_b0_v1_250129_whitelist.vcf.gz"

mkdir -p amber/filtered_vcfs/chr${chr}
bcftools view --regions-overlap 0 --regions "$region" -S "$whitelist_path" -Oz -o "$out" "$vcf_path"
