import argparse
import numpy as np
import os
import polars as pl
import linear_dag as ld
from linear_dag.core.lineararg import LinearARG
from scipy.stats import chi2


def get_statistics(linarg_dir, beta_dir, out_dir, partition_id):
    
    if not os.path.exists(f'{out_dir}/regression_statistics/'): os.makedirs(f'{out_dir}/regression_statistics/')
    
    beta_hats = np.load(f'{beta_dir}/{partition_id}_genotypes.npy')
    # beta_hats = np.load(f'{beta_dir}/{partition_id}_linarg.npy')
    linarg = ld.LinearARG.read(f'{linarg_dir}/{partition_id}/linear_arg.npz', f'{linarg_dir}/{partition_id}/linear_arg.pvar', f'{linarg_dir}/{partition_id}/linear_arg.psam')    
    df = linarg.variants.table
    N = linarg.shape[0] / 2 # roughly, maybe change this to be exact
    df = df.with_columns(pl.lit(beta_hats).alias('beta_hat'))
    df = df.with_columns(pl.lit(beta_hats*N**0.5).alias('z-score'))
    df = df.with_columns(pl.lit(beta_hats**2*N).alias('chi-squared'))
    df = df.with_columns(pl.lit(np.array([chi2.sf(x, 1) for x in beta_hats**2*N])).alias('chi-squared_pval'))
    
    df.write_csv(f'{out_dir}/regression_statistics/{partition_id}.csv')
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('linarg_dir', type=str)
    parser.add_argument('beta_dir', type=str)
    parser.add_argument('partition_id', type=str)
    parser.add_argument('out_dir', type=str)
    args = parser.parse_args()
    
    get_statistics(args.linarg_dir, args.beta_dir, args.out_dir, args.partition_id)