import numpy as np
import os

linarg_path = '/mnt/project/linear_args/ukb20279'
linarg_variant_counts = []

for i in np.arange(1, 23):
    counts = 0
    for large_partition in os.listdir(f'{linarg_path}/chr{i}'):
        for txt_file in os.listdir(f'{linarg_path}/chr{i}/{large_partition}/variant_metadata'):
            with open(f'{linarg_path}/chr{i}/{large_partition}/variant_metadata/{txt_file}', 'r') as f:
                n_variants = sum(1 for _ in f) - 1
            counts += n_variants
    linarg_variant_counts.append(counts)

    print(f'{i}: {counts}')
    
# import pysam
# vcf_paths = [f"/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c{i}_b0_v1.vcf.gz" for i in np.arange(1, 23)]
# vcf_paths = [os.path.join(base_path, f"ukb20279_c{i}_b0_v1.vcf.gz") for i in np.arange(1, 23)]
# vcf_variant_counts = [sum(1 for _ in pysam.VariantFile(vcf)) for vcf in vcf_paths]
