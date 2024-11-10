from cyvcf2 import VCF, Writer
import os

input_vcf = '/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c1_b0_v1.vcf.gz'
region = 'chr1:150000001-170000000'
output_vcf = '/linear_arg_results/20mb-500kb-window-test_chr1-150000001-170000000/vcf_file.vcf.gz'

if not os.path.exists(f'/linear_arg_results/20mb-500kb-window-test_chr1-150000001-170000000/'): os.makedirs(f'/linear_arg_results/20mb-500kb-window-test_chr1-150000001-170000000/')

vcf = VCF(input_vcf)

# Create a writer object for the output VCF file
out = Writer(output_vcf, vcf)

# Iterate through the variants in the specified region
for variant in vcf(region):
    # Write each variant to the output file
    out.write_record(variant)

# Close the writer and input VCF file
out.close()
vcf.close()