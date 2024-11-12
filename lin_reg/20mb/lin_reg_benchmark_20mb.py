import scipy.sparse as sp
import argparse
import numpy as np
import os
import time
import polars as pl
import linear_dag as ld
from linear_dag.brick_graph import read_brick_graph_npz
from linear_dag.recombination import Recombination
from linear_dag.one_summed_cy import linearize_brick_graph
from linear_dag.lineararg import VariantInfo, LinearARG


def load_linarg(linarg_dir, partition_id):
    start = time.time()    
    linarg = ld.LinearARG.read(f'{linarg_dir}/{partition_id}/linear_arg.npz', f'{linarg_dir}/{partition_id}/linear_arg.pvar', f'{linarg_dir}/{partition_id}/linear_arg.psam')    
    linarg = linarg.make_triangular()
    end = time.time()
    return linarg, end-start


def load_genotypes(linarg_dir, partition_id):
    start = time.time()
    mtx_files = os.listdir(f'{linarg_dir}/{partition_id}/genotype_matrices/')
    ind_arr = np.array([int(f.split('_')[0]) for f in mtx_files])
    order = ind_arr.argsort()
    mtx_files = np.array(mtx_files)[order].tolist() # sort files by index
    genotypes = sp.hstack([sp.load_npz(f'{linarg_dir}/{partition_id}/genotype_matrices/{m}') for m in mtx_files])   
    end = time.time() 
    return genotypes, end-start
    

def run_regression(X, data_type, partition_id):
        
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
        allele_counts =  ((np.ones(N) @ S) @ X)
    xTx = 2 / N * allele_counts * (N - allele_counts) # 2Npq
    effect_sizes_linarg = xTy / xTx
    end = time.time()
    
    return end-start, N, M


def benchmark_regression(linarg_dir, partition_id, data_type, res_dir):
    
    if not os.path.exists(f'{res_dir}/'): os.makedirs(f'{res_dir}/')

    if data_type == 'linarg':
        linarg, load_time = load_linarg(linarg_dir, partition_id)
        reg_time, N, M = run_regression(linarg, 'linarg', partition_id)
    else:
        genotypes, load_time = load_genotypes(linarg_dir, partition_id)
        reg_time, N, M = run_regression(genotypes, 'genotypes', partition_id)
        
    with open(f'{res_dir}/{partition_id}_{data_type}.txt', 'w') as file:
        file.write(" ".join(['partition_id', 'data_type', 'n', 'm', 'load_time', 'reg_time'])+'\n')
        file.write(" ".join([partition_id, data_type, str(N), str(M), str(np.round(load_time, 3)), str(np.round(reg_time, 3))])+'\n')
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('linarg_dir', type=str)
    parser.add_argument('partition_id', type=str)
    parser.add_argument('data_type', type=str)
    parser.add_argument('res_dir', type=str)
    args = parser.parse_args()
    
    benchmark_regression(args.linarg_dir, args.partition_id, args.data_type, args.res_dir)