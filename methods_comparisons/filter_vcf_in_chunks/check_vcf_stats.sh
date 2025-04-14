#!/bin/bash

VCF_FILE="$1"

# Number of samples
NUM_SAMPLES=$(bcftools query -l "$VCF_FILE" | wc -l)

# Number of variants (requires index)
NUM_VARIANTS=$(bcftools index --nrecords "$VCF_FILE")

echo "VCF File: $VCF_FILE"
echo "Samples: $NUM_SAMPLES"
echo "Variants: $NUM_VARIANTS"
