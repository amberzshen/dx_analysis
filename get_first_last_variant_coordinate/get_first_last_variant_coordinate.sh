#!/bin/bash

chroms=({1..22})
# chroms=({1..3})
first_coords=()
last_coords=()

genome_lengths="/mnt/project/GRCh38_metadata/GRCh38_genome_lengths.txt"

for chrom in "${chroms[@]}"; do

        echo $chrom

        vcf_path="/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c${chrom}_b0_v1.vcf.gz"

        first_coord=$(bcftools view -G -H "$vcf_path" | head -1 |  awk '{print $2}')
        first_coords+=($first_coord)

        end=$(($(awk 'NR==i {print $j}' i=$chrom j=2 $genome_lengths) + 500000))
        start=$(($end - 1000000))
        last_coord=$(bcftools query -r "chr${chrom}:${start}-${end}" "$vcf_path" -f "%POS\n" | tail -n 1)
        last_coords+=($last_coord)

done
echo "${first_coords[@]}"
echo "${last_coords[@]}"

for i in "${!chroms[@]}"; do
    chrom=$(($i+1))
    echo "chr${chrom} ${first_coords[$i]} ${last_coords[$i]}" >> GRCh38_first_last_variant_coordinate.txt
done
