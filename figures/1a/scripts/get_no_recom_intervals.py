import numpy as np
import h5py
import scipy.sparse as sp


def make_tree(genotypes):
    # iterate through variants like brick graph algorithm
    pass

def consolidate_haplotypes(genotypes, interval):
    genotypes_interval = genotypes[:, interval[0]:interval[1]+1] # inclusive
    unique_haplotypes, haplotype_counts = np.unique(genotypes_interval, axis=0, return_counts=True)
    return unique_haplotypes, haplotype_counts


def sort_intervals(intervals):
    return sorted(intervals, key=lambda x: x[1] - x[0] + 1, reverse=True)
    
    
def get_no_recom_intervals(genotypes):
    genotypes_t = genotypes.T
    intervals = [] # intervals with no recombination
    for i in range(genotypes.shape[1]):
        intervals.append([i, i]) # start a new interval
        v1 = np.array(genotypes_t[i]).ravel()
        for interval in [x for x in intervals if x[1]+1 == i]:
            passes = True
            for j in range(interval[0], interval[1]+1):
                v2 = np.array(genotypes_t[j]).ravel()
                if not four_gametes_test(v1, v2):
                    passes = False
                    break
            if passes:
                interval[1] += 1
    return intervals

    
def four_gametes_test(a, b, strict=True):
    gametes = set(np.unique(a * 2 + b))
    if strict:
        failing_condition = {1, 2, 3}.issubset(gametes) # 10, 01, 11
    else:
        failing_condition = len(gametes) == 4 # 00, 10, 01, 11
    if failing_condition:
        return False
    else:
        return True
    
    
if __name__ == "__main__":
    
    with h5py.File("/Users/ambershen/Desktop/linARG/dx_analysis/figures/1a/data/genotype_matrices/0_chr2-234000000-236000000.h5", 'r') as f:
        genotypes = sp.csc_matrix((f['data'][:], f['indices'][:], f['indptr'][:]), shape=f['shape'][:]) 
    genotypes = genotypes.todense()
    
    intervals = get_no_recom_intervals(genotypes)
    sorted_intervals = sort_intervals(intervals)

    for i in sorted_intervals[:10]:
        genotypes_cons, counts = consolidate_haplotypes(genotypes, i)
        print(f'interval: {i}')
        print(f'unique haplotypes shape: {genotypes_cons.shape}')
        print(f'unique haplotypes nnz: {np.count_nonzero((genotypes_cons))}')
        print(f'haplotype counts: {counts}')
        print(genotypes_cons)
        print()