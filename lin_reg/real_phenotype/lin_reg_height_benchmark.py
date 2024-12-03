import scipy.sparse as sp
import argparse
import numpy as np
import os
import time
import polars as pl
import linear_dag as ld
from linear_dag.lineararg import LinearARG
import pandas as pd


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


def get_phenotype_vector(phenotype, phenotypes, sample_ids):
    
    N = len(sample_ids)
    
    ind_to_sample = {i: int(sample_ids[i]) if sample_ids[i].isdigit() else None for i in range(N)}
    phenotypes = phenotypes[phenotypes.eid.isin(ind_to_sample.values())]
    sample_to_phenotype = {r.eid: r[phenotype] for _,r in phenotypes.iterrows()}

    phenotype_vector = np.full((N, 1), np.nan)
    for i in range(N):
        if ind_to_sample[i] != None:
            phenotype_vector[i] = sample_to_phenotype[ind_to_sample[i]] 

    samples_to_remove = np.where(np.isnan(phenotype_vector))[0] # either individual has withdrawn or phenotype is missing

    data = np.ones(N-len(samples_to_remove))
    row_indices = np.arange(N-len(samples_to_remove))
    col_indices = np.setdiff1d(np.arange(N), samples_to_remove)
    R = sp.csr_matrix((data, (row_indices, col_indices)), shape=(N-len(samples_to_remove), N))

    phenotype_vector = phenotype_vector[~np.isnan(phenotype_vector)]
    phenotype_vector = phenotype_vector - np.mean(phenotype_vector)
    phenotype_vector = phenotype_vector / np.std(phenotype_vector)
    
    return phenotype_vector, R


def get_sum_matrix(N, M):
    data = np.ones(2*N)
    row_indices = np.repeat(np.arange(N), 2)
    col_indices = np.arange(2*N)
    S = sp.csr_matrix((data, (row_indices, col_indices)), shape=(N, 2*N))
    return S
    

def linarg_regression(linarg, y, R):
    
    N_total = int(linarg.shape[0] / 2)
    M = int(linarg.shape[1])
    S = get_sum_matrix(N_total, M)
    N = R.shape[0]

    start = time.time()
    X = sp.linalg.aslinearoperator(R) @ sp.linalg.aslinearoperator(S) @ linarg # normalize
    xTy = X.rmatvec(y.T) # divide by sqrt(2)
    
    # allele_counts = X.rmatvec((np.ones(N)).T)
    # xTx = 2 / N * allele_counts * (N - allele_counts) # 2Npq (function for this)
    
    # effect_sizes_linarg = xTy / xTx
    end = time.time()
    
    # save and download effect sizes
    
    return end-start, N, M


def genotypes_regression(genotypes, y, R):
    
    N_total = int(genotypes.shape[0] / 2)
    M = int(genotypes.shape[1])
    S = get_sum_matrix(N_total, M)
    N = R.shape[0]
    
    start = time.time()
    xTy = y @ R @ S @ genotypes
    allele_counts =  np.ones(R.shape[0]) @ R @ S @ genotypes
    xTx = 2 / N * allele_counts * (N - allele_counts) # 2Npq
    effect_sizes_linarg = xTy / xTx
    end = time.time()
    
    return end-start, N, M


def benchmark_regression(linarg_dir, partition_id, data_type, res_dir):
    
    if not os.path.exists(f'{res_dir}/'): os.makedirs(f'{res_dir}/')
    
    # hard code this for now
    phenotype = 'p50_i0' # height
    phenotypes = pd.read_csv('/mnt/project/phenotypes/age_sex_height_lymphcnt_participant.csv')
    with open('/mnt/project/linear_args/ukb20279/sample_ids.txt', 'r') as file:
        sample_ids = [line.strip() for line in file]
    y, R = get_phenotype_vector(phenotype, phenotypes, sample_ids)
    
    if data_type == 'linarg':
        linarg, load_time = load_linarg(linarg_dir, partition_id)
        reg_time, N, M = linarg_regression(linarg, y, R)
    else:
        genotypes, load_time = load_genotypes(linarg_dir, partition_id)
        reg_time, N, M = genotypes_regression(genotypes, y, R)
        
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