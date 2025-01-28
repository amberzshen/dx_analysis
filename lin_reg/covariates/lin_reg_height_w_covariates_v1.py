import scipy.sparse as sp
import argparse
import numpy as np
import os
import time
import polars as pl
import linear_dag as ld
from linear_dag.core.lineararg import LinearARG
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


def get_phenotype_covariates(phenotype, covariates, phenotypes, sample_ids):
    
    phenotypes = phenotypes[['eid', phenotype]+covariates]
    N = len(sample_ids)
    sample_to_ind = {phenotypes.eid[i]: i for i in range(phenotypes.shape[0])}
    order = np.full((phenotypes.shape[0], 1), np.nan) # map dataframe rows to sample_ids order
    samples_to_remove = []
    
    for i in range(N):
        if not sample_ids[i].isdigit():
            samples_to_remove.append(i) # remove withdrawn samples
        else:
            order[sample_to_ind[int(sample_ids[i])]] = i

    phenotypes['order'] = order
    phenotypes = phenotypes.sort_values(by='order', ascending=True)
    phenotypes = phenotypes.reset_index()
    rows_to_drop = np.where(phenotypes.isnull().any(axis=1))[0] # remove any samples with missing phenotypes or covariates
    samples_to_remove += [x for x in list(phenotypes.order[np.where(phenotypes.isnull().any(axis=1))[0]]) if not np.isnan(x)]
    phenotypes = phenotypes[~phenotypes.index.isin(rows_to_drop)]
    C = sp.csr_matrix(phenotypes[covariates].to_numpy())
    y = np.array(phenotypes[phenotype])

    data = np.ones(N-len(samples_to_remove))
    row_indices = np.arange(N-len(samples_to_remove))
    col_indices = np.setdiff1d(np.arange(N), samples_to_remove)
    R = sp.csr_matrix((data, (row_indices, col_indices)), shape=(N-len(samples_to_remove), N))
    y = y - np.mean(y)
    y = y / np.std(y)
    
    return y, C, R


def get_sum_matrix(N, M):
    data = np.ones(2*N)
    row_indices = np.repeat(np.arange(N), 2)
    col_indices = np.arange(2*N)
    S = sp.csr_matrix((data, (row_indices, col_indices)), shape=(N, 2*N))
    return S


def linarg_regression(linarg, y, R, C):
    
    N_total = int(linarg.shape[0] / 2)
    M = int(linarg.shape[1])
    S = get_sum_matrix(N_total, M)
    N = R.shape[0]

    start = time.time()
    X = sp.linalg.aslinearoperator(R) @ sp.linalg.aslinearoperator(S) @ linarg.normalized
    P = sp.linalg.aslinearoperator(sp.eye(N)) - sp.linalg.aslinearoperator(C) @ sp.linalg.aslinearoperator(sp.linalg.spsolve(C.T @ C, C.T))
    y_resid = P @ y.T
    y_resid = y_resid - np.mean(y_resid)
    y_resid = y_resid / np.std(y_resid)
    beta_hat = (X.T @ P.T @ P @ y_resid) / (2**0.5 * N)
    end = time.time()
        
    return beta_hat, end-start


def genotypes_regression(genotypes, y, R, C):
    
    N_total = int(genotypes.shape[0] / 2)
    M = int(genotypes.shape[1])
    S = get_sum_matrix(N_total, M)
    N = R.shape[0]
    
    start = time.time()
    allele_frequencies = np.ones(genotypes.shape[0]) @ genotypes / genotypes.shape[0]
    mean = sp.linalg.aslinearoperator(np.ones((genotypes.shape[0], 1))) @ sp.linalg.aslinearoperator(allele_frequencies)
    pq = allele_frequencies * (1 - allele_frequencies)
    pq[pq == 0] = 1
    G = (sp.linalg.aslinearoperator(genotypes) - mean) * sp.linalg.aslinearoperator(sp.diags(pq**-0.5))
    X = sp.linalg.aslinearoperator(R) @ sp.linalg.aslinearoperator(S) @ G    
    P = sp.linalg.aslinearoperator(sp.eye(N)) - sp.linalg.aslinearoperator(C) @ sp.linalg.aslinearoperator(sp.linalg.spsolve(C.T @ C, C.T))
    y_resid = P @ y.T
    y_resid = y_resid - np.mean(y_resid)
    y_resid = y_resid / np.std(y_resid)
    beta_hat = (X.T @ P.T @ P @ y_resid) / (2**0.5 * N)
    end = time.time()
    
    return beta_hat, end-start


def benchmark_regression(linarg_dir, partition_id, data_type, res_dir):
    
    if not os.path.exists(f'{res_dir}/'): os.makedirs(f'{res_dir}/')
    if not os.path.exists(f'{res_dir}/statistics/'): os.makedirs(f'{res_dir}/statistics/')
    if not os.path.exists(f'{res_dir}/beta_hats/'): os.makedirs(f'{res_dir}/beta_hats/')
    
    # load height data and covariates
    phenotypes = pd.read_csv('/mnt/project/phenotypes/age_sex_height_pcs.csv')
    phenotypes['sex'] = [0 if phenotypes.p31[i]=='Male' else 1 for i in range(phenotypes.shape[0])]
    with open('/mnt/project/linear_args/ukb20279/sample_ids.txt', 'r') as file:
        sample_ids = [line.strip() for line in file]
    covariates = ['p21022', 'sex'] + [f'p22009_a{i}' for i in range(1,41)]
    y, C, R = get_phenotype_covariates('p50_i0', covariates, phenotypes, sample_ids)
    
    if data_type == 'linarg':
        linarg, load_time = load_linarg(linarg_dir, partition_id)
        beta_hats, reg_time = linarg_regression(linarg, y, R, C)
    else:
        genotypes, load_time = load_genotypes(linarg_dir, partition_id)
        beta_hats, reg_time = genotypes_regression(genotypes, y, R, C)
        
    np.save(f'{res_dir}/beta_hats/{partition_id}_{data_type}.npy', beta_hats)
    with open(f'{res_dir}/statistics/{partition_id}_{data_type}.txt', 'w') as file:
        file.write(" ".join(['partition_id', 'data_type', 'load_time', 'reg_time'])+'\n')
        file.write(" ".join([partition_id, data_type, str(np.round(load_time, 3)), str(np.round(reg_time, 3))])+'\n')


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('linarg_dir', type=str)
    parser.add_argument('partition_id', type=str)
    parser.add_argument('data_type', type=str)
    parser.add_argument('res_dir', type=str)
    args = parser.parse_args()
    
    benchmark_regression(args.linarg_dir, args.partition_id, args.data_type, args.res_dir)
    
    
    