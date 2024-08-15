import linear_dag as ld
import numpy as np
import scipy.sparse
import argparse
import time

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('data_identifier', type=str)
args = parser.parse_args()

mtx_path = f'{args.data_identifier}.npz'
sparse_matrix = scipy.sparse.load_npz(mtx_path)
n, m = sparse_matrix.shape
af = np.diff(sparse_matrix.indptr) / n
incl = (af > 0) * (af < 1)
genotypes = sparse_matrix[:, incl == 1]
linarg = ld.LinearARG.from_genotypes(genotypes)

with open(f'{args.data_identifier}.txt', 'r') as f:
    lines = f.readlines()[4:] # skip header lines
    positions = []
    refs = []
    alts = []
    for line in lines:
        items = line.split()
        positions.append(items[1])
        refs.append(items[3])
        alts.append(items[4])

chrom = args.data_identifier.split('_')[1].split('chr')[1].split(':')[0]
linarg.write(f'/linear_args/adjacency_matrices/{args.data_identifier}', chrom, positions, refs, alts)

end = time.time()

runtime = end - start
nnz_ratio = np.sum(n * np.minimum(af, 1-af)) / linarg.nnz
stats = [args.data_identifier, n, m, runtime, nnz_ratio]

with open(f'linear_args/statistics/{args.data_identifier}.txt', 'w') as file:
    file.write("\t".join(stats))