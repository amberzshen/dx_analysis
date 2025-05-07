import numpy as np
import time
import linear_dag as ld
import sys
import os
from scipy.sparse import csr_matrix, csc_matrix, eye
import h5py


def main():
    
    linarg_path = '/Users/ambershen/Desktop/linARG/dx_analysis/test_pipeline/linear_args/csc/linear_arg'

    t1 = time.time()
    linarg = ld.LinearARG.read(f'{linarg_path}.h5')
    t2 = time.time()
    print(f'Time to load LinearARG: {t2 - t1:.3f} seconds')
    
    # linarg = linarg.add_individual_nodes()

    ncol = 100
    print(f"Number of columns: {ncol}")

    print(f"LinearARG shape: {linarg.shape}")

    t1 = time.time()
    linarg.calculate_nonunique_indices()
    t2 = time.time()
    print(f'Time to calculate nonunique indices: {t2 - t1:.3f} seconds')
    
    b = np.arange(ncol * linarg.shape[1]).reshape((-1, ncol)).astype(np.float32)
    # b = np.random.normal(size=ncol * linarg.shape[1]).reshape((-1, ncol)).astype(np.float32)

    t_start = time.time()
    result_matmat_true = np.column_stack([linarg @ b[:, i] for i in range(b.shape[1])])
    t_end = time.time()
    print(f"Time for linarg @ b column by column: {t_end - t_start:.3f} seconds")

    linarg.A = csc_matrix(linarg.A)
    t_start = time.time()
    result_fp32 = linarg @ b
    t_end = time.time()
    print(f"Time for linarg @ b block fp32: {t_end - t_start:.3f} seconds")

    print(f'matvec: {result_matmat_true.ravel()}')
    print(f'matmat: {result_fp32.ravel()}')
    print(f'diff: {result_fp32.ravel() - result_matmat_true.ravel()}')
    # assert np.allclose(result_fp32.ravel(), result_matmat_true.ravel()), "Results do not match"

    t_start = time.time()
    result_scipy = linarg._matmat_scipy(b)
    t_end = time.time()
    print(f"Time for linarg @ b scipy fp32: {t_end - t_start:.3f} seconds")
    
    b = b.astype(np.float64)
    
    t_start = time.time()
    result_matmat_true = np.column_stack([linarg @ b[:, i] for i in range(b.shape[1])])
    t_end = time.time()
    print(f"Time for linarg @ b column by column: {t_end - t_start:.3f} seconds")
    
    t_start = time.time()
    result_fp64 = linarg @ b
    t_end = time.time()
    print(f"Time for linarg @ b block fp64: {t_end - t_start:.3f} seconds")
    
    print(f'matvec: {result_matmat_true.ravel()}')
    print(f'matmat: {result_fp64.ravel()}')
    print(f'diff: {result_fp64.ravel() - result_matmat_true.ravel()}')
    print(f'scipy: {result_scipy.ravel()}')
    assert np.allclose(result_fp64.ravel(), result_matmat_true.ravel()), "Results do not match"
    
    print("Results match for matmat with multiple rows\n")

    y = np.arange(ncol * linarg.shape[0]).reshape((ncol, -1)).astype(np.float32)

    t_start = time.time()
    result_rmatmat_true = np.vstack([y[i,:] @ linarg for i in range(y.shape[0])])
    t_end = time.time()
    print(f"Time for y @ linarg row by row: {t_end - t_start:.3f} seconds")

    t_start = time.time()
    result_fp32 = y @ linarg
    t_end = time.time()
    print(f"Time for y @ linarg block fp32: {t_end - t_start:.3f} seconds")

    print(f'matvec: {result_rmatmat_true.ravel()}, {result_rmatmat_true.ravel().shape}')
    print(f'matmat: {result_fp32.ravel()}, {result_fp32.ravel().shape}')
    print(f'diff: {result_fp32.ravel() - result_rmatmat_true.ravel()}')
    # assert np.allclose(result_rmatmat_true.ravel(), result_fp32.ravel()), "Results do not match"

    y = y.astype(np.float64)
    t_start = time.time()
    result_fp64 = y @ linarg
    t_end = time.time()
    print(f"Time for y @ linarg block fp64: {t_end - t_start:.3f} seconds")
    
    print(f'matvec: {result_rmatmat_true.ravel()}')
    print(f'matmat: {result_fp64.ravel()}')
    print(f'diff: {result_fp64.ravel() - result_rmatmat_true.ravel()}')
    assert np.allclose(result_rmatmat_true.ravel(), result_fp64.ravel()), "Results do not match"
    print("Results match for rmatmat with multiple columns\n")



if __name__ == "__main__":
    main()