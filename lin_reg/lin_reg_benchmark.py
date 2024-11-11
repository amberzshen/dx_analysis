import scipy.sparse as sp
import argparse
import numpy as np
import os
import time
import linear_dag as ld
from linear_dag.brick_graph import read_brick_graph_npz


def load_linarg(linarg_dir, partition_id):    
    brick_graph, sample_indices, variant_indices = read_brick_graph_npz(np.load(f'{linarg_dir}/brick_graph_partitions/{partition_id}.npz'))
    brick_graph_recom = Recombination.from_graph(brick_graph)
    brick_graph_recom.find_recombinations()
    linear_arg_adjacency_matrix = linearize_brick_graph(brick_graph_recom)
    var_info = pl.read_csv(f'{linarg_dir}/variant_metadata/{partition_id}.txt', separator=' ')
    var_info = var_info.with_columns(variant_indices.alias('IDX'))
    linarg = LinearARG(linear_arg_adjacency_matrix, sample_indices, var_info)
    linarg = linarg.make_triangular()
    return linarg


def load_genotypes(linarg_dir, partition_id):
    genotypes = sp.load_npz(f'{linarg_dir}/genotype_matrices/{partition_id}.npz')
    return genotypes
    

def run_regression(X, data_type, partition_id, res_dir):
    
    N = int(X.shape[0] / 2)
    M = int(X.shape[1])

    data = np.ones(2*N)
    row_indices = np.repeat(np.arange(N), 2)
    col_indices = np.arange(2*N)
    S = sp.csr_matrix((data, (row_indices, col_indices)), shape=(N, 2*N))

    np.random.seed(int(partition_id.split('_')[0]))
    y = np.random.normal(0, 1, N)

    start = time.time()
    if data_type == 'linarg':
        xTy = ((y @ S) @ X) [0]
        allele_counts =  ((np.ones(N) @ S) @ X) [0]
    else:
        xTy = ((y @ S) @ X)
        allele_counts =  ((np.ones(N) @ S) @ linarg)
    xTx = 2 / N * allele_counts * (N - allele_counts) # 2Npq
    effect_sizes_linarg = xTy / xTx
    end = time.time()

    with open(f'{res_dir}/{partition_id}_{data_type}.txt', 'w') as file:
        file.write(" ".join([partition_id, data_type, 'n', 'm', 'time'])+'\n')
        file.write(" ".join([str(N), str(M), str(np.round(end-start, 3))])+'\n')


def benchmark_regression(linarg_dir, partition_id, data_type, res_dir):
    if data_type == 'linarg':
        linarg = load_linarg(linarg_dir, partition_id)
        run_regression(linarg, 'linarg', partition_id, res_dir)
    else:
        genotypes = load_genotypes(linarg_dir, partition_id)
        run_regression(genotypes, 'genotypes', partition_id, res_dir)
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('linarg_dir', type=str)
    parser.add_argument('partition_id', type=str)
    parser.add_argument('data_type', type=str)
    parser.add_argument('res_dir', type=str)
    args = parser.parse_args()
    
    benchmark_regression(args.linarg_dir, args.partition_id, args.data_type, args.res_dir)