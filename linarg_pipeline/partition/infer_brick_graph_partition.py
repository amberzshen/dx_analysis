import linear_dag as ld
import numpy as np
import scipy.sparse
import argparse
import time

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('partition_identifier', type=str)
args = parser.parse_args()

mtx_path = f'{args.partition_identifier}.npz'
sparse_matrix = scipy.sparse.load_npz(mtx_path)
n, m = sparse_matrix.shape
af = np.diff(sparse_matrix.indptr) / n
genotypes = sparse_matrix

brick_graph, samples_idx, variants_idx = ld.BrickGraph.from_genotypes(genotypes)
recom = ld.Recombination.from_graph(brick_graph)
recom.find_recombinations()
adj_mat = recom.to_csr()

np.savez(f'brick_graph_partitions/{args.partition_identifier}.npz',
        brick_graph_data=adj_mat.data,
        brick_graph_indices=adj_mat.indices,
        brick_graph_indptr=adj_mat.indptr,
        brick_graph_shape=adj_mat.shape,
        sample_indices=np.array(samples_idx),
        variant_indices=np.array(variants_idx))

end = time.time()

runtime = end - start
geno_nnz = np.sum(n * np.minimum(af, 1-af))
nnz_ratio = geno_nnz / adj_mat.nnz
stats = [args.partition_identifier, str(n), str(m), str(runtime), str(geno_nnz), str(adj_mat.nnz), str(nnz_ratio)]

# separate times for each step
with open(f'brick_graph_partition_stats/{args.partition_identifier}.txt', 'w') as file:
    file.write("\t".join(['partition_identifier', 'n', 'm', 'runtime', 'geno_nnz', 'brickgraph_nnz', 'nnz_ratio'])+'\n')
    file.write("\t".join(stats)+'\n')