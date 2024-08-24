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

brick_graph, samples_idx, variants_idx = ld.BrickGraph.from_genotypes(genotypes)
recom = ld.Recombination.from_graph(brick_graph)
recom.find_recombinations()
adj_mat = recom.to_csr()

np.savez(f'linear_arg_partitions/{args.data_identifier}.npz',
        brick_graph_adj_mat=recom.to_csr(),
        sample_indices=np.array(samples_idx),
        variant_indices=np.array(variants_idx))

end = time.time()

runtime = end - start
geno_nnz = np.sum(n * np.minimum(af, 1-af))
nnz_ratio = geno_nnz / adj_mat.nnz
stats = [args.data_identifier, str(n), str(m), str(runtime), str(geno_nnz), str(adj_mat.nnz), str(nnz_ratio)]

with open(f'linear_arg_partition_stats/{args.data_identifier}.txt', 'w') as file:
    file.write("\t".join(['data_identifier', 'n', 'm', 'runtime', 'geno_nnz', 'brickgraph_nnz', 'nnz_ratio']))
    file.write("\t".join(stats))