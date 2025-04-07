import os
import h5py
import linear_dag as ld
import time
import scipy.sparse as sp
import polars as pl
import numpy as np
import pandas as pd
import hdf5plugin


def write_hdf5(linarg, filename, shuffle=True, compression_option="lzf", save_data=True, save_indices=False):
    
    csr_matrix = linarg.A
    sample_indices = linarg.sample_indices
    variant_indices = linarg.variant_indices
    flip = linarg.variants.is_flipped

    with h5py.File(filename, 'w') as f:
        f.attrs['n'] = csr_matrix.shape[0]
        f.create_dataset('indptr', data=csr_matrix.indptr, compression=compression_option, shuffle=shuffle)
        f.create_dataset('indices', data=csr_matrix.indices, compression=compression_option, shuffle=shuffle)
        if save_data:
            f.create_dataset('data', data=csr_matrix.data, compression=compression_option, shuffle=shuffle)
        if save_indices:
            f.create_dataset('sample_indices', data=sample_indices, compression=compression_option, shuffle=shuffle)
            f.create_dataset('variant_indices', data=variant_indices, compression=compression_option, shuffle=shuffle)
            f.create_dataset('flip', data=flip, compression=compression_option, shuffle=shuffle)
         
            
def read_hdf5_mtx_no_data(h5_path):
    with h5py.File(h5_path, 'r') as f:
        A = sp.csr_matrix((np.ones(len(f['indices'][:])), f['indices'][:], f['indptr'][:]), shape=(f.attrs['n'], f.attrs['n']))
    return A


def read_hdf5_mtx(h5_path):
    with h5py.File(h5_path, 'r') as f:
        A = sp.csr_matrix((f['data'][:], f['indices'][:], f['indptr'][:]), shape=(f.attrs['n'], f.attrs['n']))
    return A


def read_hdf5_linarg(h5_path):
    with h5py.File(h5_path, 'r') as f:
        A = sp.csr_matrix((f['data'][:], f['indices'][:], f['indptr'][:]), shape=(f.attrs['n'], f.attrs['n']))
        sample_indices = f['sample_indices'][:]
        variant_indices = f['variant_indices'][:]
        flip = f['flip'][:]
    return A, sample_indices, variant_indices, flip


if __name__ == "__main__":
    
    t1 = time.time()
    linarg = ld.LinearARG.read(f"linear_arg.npz", f"linear_arg.pvar.gz", f"linear_arg.psam.gz")
    t2 = time.time()

    t3 = time.time()
    A = sp.load_npz(f"linear_arg.npz")
    t4 = time.time()

    npz_disk_size = os.path.getsize(f"linear_arg.npz") / 10**6
    linarg_disk_size = npz_disk_size + (os.path.getsize(f"linear_arg.pvar.gz") + os.path.getsize(f"linear_arg.psam.gz")) / 10**6
    df = pd.DataFrame({'data_type': ['linarg', 'mtx'], 'compression_type': ['npz', 'npz'], 'disk_size': [linarg_disk_size, npz_disk_size], 'load_time': [t2-t1, t4-t3]})

    h5_path = 'test.h5'
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
            
        for d in ['linarg', 'mtx', 'mtx_no_data']:
            
            if d == 'linarg':
                write_hdf5(linarg, h5_path, shuffle=True, compression_option=compression, save_data=True, save_indices=True)
                t3 = time.time()
                linarg_h5 = read_hdf5_linarg(h5_path)
                t4 = time.time()
            elif d == 'mtx':
                write_hdf5(linarg, h5_path, shuffle=True, compression_option=compression, save_data=True, save_indices=False)
                t3 = time.time()
                A_h5 = read_hdf5_mtx(h5_path)
                t4 = time.time()
            elif d == 'mtx_no_data':
                write_hdf5(linarg, h5_path, shuffle=True, compression_option=compression, save_data=False, save_indices=False)
                t3 = time.time()
                A_h5 = read_hdf5_mtx_no_data(h5_path)
                t4 = time.time()

            h5_disk_size = os.path.getsize(h5_path) / 10**6
            df.loc[df.shape[0]] = [d, c, h5_disk_size, t4-t3]
    
    os.remove(h5_path)
    df.to_csv('compression_option_results.csv', index=False)