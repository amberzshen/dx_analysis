import numpy as np
import os


# start and end are inclusive
def get_partitions(interval_start, interval_end, partition_size):
    num_partitions = int((interval_end - interval_start + 1) / partition_size)
    ticks = np.linspace(interval_start, interval_end+1, num_partitions+1).astype(int)
    ends = ticks[1:] - 1
    starts = ticks[:-1]
    intervals = [(start, end) for start,end in zip(starts, ends)]
    # print(f'size of intervals: {[x[1]-x[0]+1 for x in intervals]}')
    return intervals


def partition_chromosome(chrom, chrom_start, chrom_end, partition_size, out):
    partitions = get_partitions(chrom_start, chrom_end, partition_size)
    with open(f'{out}partitions.txt', 'w') as f:
        f.write(' '.join(['chrom', 'partition_number', 'start', 'end'])+'\n')
        for i in range(len(partitions)):
            partition = [chrom, i, partitions[i][0], partitions[i][1]]
            f.write(' '.join([str(x) for x in partition])+'\n')

    

if __name__ == "__main__":
    
    ### testing ###
    # chrom = 6
    # chrom_start = 32578775
    # chrom_end = 33578776
    # partition_size = 1e4
    # out = 'test'
    # os.makedirs(out, exist_ok = True)
    # partition_chromosome(chrom, chrom_start, chrom_end, partition_size, f'{out}/chr6_')
    
    partition_size = 1e6
    out = 'partitions/'
    
    os.makedirs(out, exist_ok = True)
    
    partition_chromosome(1, 15916, 248945618, partition_size, f'{out}/chr1_')
    partition_chromosome(11, 103091, 135076590, partition_size, f'{out}/chr11_')