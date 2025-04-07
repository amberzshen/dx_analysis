import os
import h5py
import linear_dag as ld
import time
import scipy.sparse as sp
import polars as pl
import numpy as np
import pandas as pd


if __name__ == "__main__":
    
    linarg_dir = '/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/no_filter'
        
    npz_path = f"{linarg_dir}/linear_arg.npz"
    pvar_path = f"{linarg_dir}/linear_arg.pvar.gz"
    sample_path = f"{linarg_dir}/linear_arg.psam.gz"
    
    start = time.time()
    linarg = ld.LinearARG.read(npz_path, pvar_path, sample_path)
    end = time.time()
    print(f'time to load linear ARG: {np.round(end-start, 3)}')

    start = time.time()
    A = sp.load_npz(npz_path)
    end = time.time()
    print(f'time to load A: {np.round(end-start, 3)}')
    
    start = time.time()
    variant_info = ld.core.lineararg.VariantInfo.read(pvar_path)
    end = time.time()
    print(f'time to load variant metadata: {np.round(end-start, 3)}')

    start = time.time()
    sample_info = pl.read_csv(sample_path, separator=" ")
    end = time.time()
    print(f'time to load sample metadata: {np.round(end-start, 3)}')
    
    
    