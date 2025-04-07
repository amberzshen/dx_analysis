import os
import h5py
import linear_dag as ld
import time
import scipy.sparse as sp
import polars as pl
import numpy as np
import pandas as pd
import hdf5plugin

def write_hdf5(linarg, filename, shuffle=True, compression_option="lzf", save_data=True):

    csr_matrix = linarg.A

    with h5py.File(filename, 'w') as f:
        f.attrs['n'] = csr_matrix.shape[0]
        f.create_dataset('indptr', data=csr_matrix.indptr, compression=compression_option, shuffle=shuffle)
        f.create_dataset('indices', data=csr_matrix.indices, compression=compression_option, shuffle=shuffle)
        if save_data:
            f.create_dataset('data', data=csr_matrix.data, compression=compression_option, shuffle=shuffle)


def read_hdf5(h5_path, variant_fname, samples_fname):
    with h5py.File(h5_path, 'r') as f:
        A = sp.csr_matrix((f['data'][:], f['indices'][:], f['indptr'][:]), shape=(f.attrs['n'], f.attrs['n']))
    sample_info = pl.read_csv(samples_fname, separator=" ")
    sample_indices = np.array(sample_info["IDX"])
    v_info = ld.core.lineararg.VariantInfo.read(variant_fname)
    linarg = ld.LinearARG(A, sample_indices, v_info)
    return linarg


if __name__ == "__main__":
    
    linarg_dir = '/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/no_filter'

    t1 = time.time()
    linarg = ld.LinearARG.read(f"linear_arg.npz", f"linear_arg.pvar.gz", f"linear_arg.psam.gz")
    t2 = time.time()

    npz_used = os.path.getsize(f"linear_arg.npz")

    h5_path = 'test.h5'

    df = pd.DataFrame({'compression_type': ['npz'], 'disk_size': [npz_used/10**9], 'load_time': [t2-t1]})

    compression = ['Blosc', 'Blosc2', 'BZip2', 'gzip', 'lzf', None]
    for c in compression:
        
        try:
            os.remove(h5_path)
        except:
            print('does not exist')
        
        if c in ['gzip', 'lzf', None]:
            compression = c
        else:
            compression = getattr(hdf5plugin, c)()
        
        write_hdf5(linarg, h5_path, compression_option=compression, save_data=True)

        h5_used = os.path.getsize(h5_path)
        t3 = time.time()
        linarg_h5 = read_hdf5(h5_path, f"linear_arg.pvar.gz", f"linear_arg.psam.gz",)
        t4 = time.time()

        print(c)
        print(f'h5 file size: {np.round(h5_used/10**9,4)}GB, npz file size: {np.round(npz_used/10**9,4)}GB')
        print(f'h5 load time: {np.round(t4-t3, 3)}s, npz load time: {np.round(t2-t1, 3)}s')
        
        df.loc[df.shape[0]] = [c, h5_used/10**9, t4-t3]
    
    os.remove(h5_path)
    df.to_csv('compression_option_results.csv', index=False)