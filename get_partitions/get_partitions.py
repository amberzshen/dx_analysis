from cyvcf2 import VCF
import numpy as np
import argparse

def get_partitions(vcf_path, region, window_size):
    
    chrom = region.split('chr')[1].split('-')[0]
    start = int(region.split("-")[1])
    region_formatted = f'{region.split("-")[0]}:{region.split("-")[1]}-{region.split("-")[2]}'

    vcf = VCF(vcf_path)
    positions = []
    for variant in vcf(region_formatted):
        positions.append(variant.POS)
    positions = np.array(positions)

    partition_starts = []
    partition_ends = []
    n_variants = []
    while len(positions) > 0:
        if len(positions) >= window_size:
            end = positions[window_size-1]
        else:
            end = positions[-1]
        positions_new = positions[np.where(positions>end)]
        partition_starts.append(start)
        partition_ends.append(end)
        n_variants.append(len(positions) - len(positions_new))
        start = end + 1
        positions = positions_new
        
    with open('partitions.txt', 'w') as f:
        f.write(' '.join(['partition', 'start', 'end', 'n_variants'])+'\n')
        for i in range(len(partition_starts)):
            partition = [i, partition_starts[i], partition_ends[i], n_variants[i]]
            f.write(' '.join([str(x) for x in partition])+'\n')
            
            
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('region', type=str)
    parser.add_argument('window_size', type=int)
    args = parser.parse_args()
    
    chrom = args.region.split('chr')[1].split('-')[0]
    vcf_path = f'/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c{chrom}_b0_v1.vcf.gz'

    get_partitions(vcf_path, args.region, args.window_size)