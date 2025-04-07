#!/bin/bash

chroms=({1..22})
variant_counts=()

output_file="UKB200k_variant_counts.txt"
echo -e "Chromosome\tFirst_Coord\tLast_Coord\tVariant_Count" > "$output_file"

for chrom in "${chroms[@]}"; do
    echo "Processing chromosome $chrom..."
    
    vcf_path="/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c${chrom}_b0_v1.vcf.gz"

    # Get the number of variants using bcftools index
    variant_count=$(bcftools index --nrecords "$vcf_path")
    variant_counts+=($variant_count)
    
    echo -e "chr${chrom}\t${first_coord}\t${last_coord}\t${variant_count}" >> "$output_file"
done

echo "Variant counts written to $output_file"