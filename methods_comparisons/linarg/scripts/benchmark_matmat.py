import linear_dag as ld
import numpy as np
import pandas as pd
import time
import os
import scipy.sparse as sp


def load_linarg(linarg_dir, partition_id):
    start = time.time()
    linarg = ld.LinearARG.read(f'{linarg_dir}/{partition_id}/linear_arg.npz', f'{linarg_dir}/{partition_id}/linear_arg.pvar.gz', f'{linarg_dir}/{partition_id}/linear_arg.psam.gz')    
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


def matmat(X, v):
    if X.shape[1] == v.shape[0]:
        start = time.time()
        u = X @ v
        end = time.time()
    elif linarg.shape[0] == v.shape[0]:
        start = time.time()
        u = X.T @ v
        end = time.time()
    else:
        print('dimensions do not match')
        return None
    return end - start


def matvec(X, v):
    if X.shape[1] == v.shape[0]:
        start = time.time()
        for i in range(v.shape[1]):
            u = X @ v[:, i]
        end = time.time()
        return end - start
    elif linarg.shape[0] == v.shape[0]:
        start = time.time()
        for i in range(v.shape[1]):
            u = X.T @ v[:, i]
        end = time.time()
        return end - start
    else:
        print('dimensions do not match')
        return None
       
    
def benchmark_dot_product(linarg, genotypes, n_vectors):
    df = pd.DataFrame(columns=['method', 'dot_product_type', 'n', 'time'])
    
    for n in n_vectors:
        
        y = np.random.normal(size=(linarg.shape[0], n))
        beta = np.random.normal(size=(linarg.shape[1], n))
        
        print(f'linarg matmat right: {n}', flush=True)
        linarg_matmat_right = matmat(linarg, beta)
        print(f'linarg matmat left: {n}', flush=True)
        linarg_matmat_left = matmat(linarg, y)
        
        print(f'linarg matvec right: {n}', flush=True)
        linarg_matvec_right = matvec(linarg, beta)
        print(f'linarg matvec left: {n}', flush=True)
        linarg_matvec_left = matvec(linarg, y)
        
        print(f'geno matmat right: {n}', flush=True)
        geno_matmat_right = matmat(genotypes, beta)
        print(f'geno matmat left: {n}', flush=True)
        geno_matmat_left = matmat(genotypes, y)
        
        df.loc[df.shape[0]] = ['linarg_matmat', 'right', n, linarg_matmat_right]
        df.loc[df.shape[0]] = ['linarg_matmat', 'left', n, linarg_matmat_left]
        df.loc[df.shape[0]] = ['linarg_matvec', 'right', n, linarg_matvec_right]
        df.loc[df.shape[0]] = ['linarg_matvec', 'left', n, linarg_matvec_left]
        df.loc[df.shape[0]] = ['genotypes', 'right', n, geno_matmat_right]
        df.loc[df.shape[0]] = ['genotypes', 'left', n, geno_matmat_left]
    
    return df

        
if __name__ == "__main__":
    
    print(f'running benchmark matmat', flush=True)
    
    # linarg_dir = '/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/'
    # partition_id = 'no_filter'
    
    linarg_dir = '/mnt/project/linear_args/ukb20279/chr21/'
    partition_id = '0_chr21-5030618-25863389'

    
    linarg, linarg_load_time = load_linarg(linarg_dir, partition_id)
    print(f'linear ARG loaded in {np.round(linarg_load_time, 3)}s', flush=True)
    genotypes, genotypes_load_time = load_genotypes(linarg_dir, partition_id)
    print(f'genotypes loaded in {np.round(genotypes_load_time, 3)}s', flush=True)
    
    n_vectors = [2, 5, 10]
    # n_vectors = [2, 5, 10, 100, 1000]
    df = benchmark_dot_product(linarg, genotypes, n_vectors)
    
    df.to_csv('matmat_benchmark_results.csv', index=False)