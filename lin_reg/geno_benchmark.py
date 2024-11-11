import scipy.sparse as sp
import numpy as np
import os
import time
import linear_dag as ld

linarg_dir = '/mnt/project/linear_args/ukb20279/chr1'

files = os.listdir(f'{linarg_dir}')
ind_arr = np.array([int(f.split('_')[0]) for f in files])
order = ind_arr.argsort()
files = np.array(files)[order].tolist() # sort files by index

f = files[0]

linarg = ld.LinearARG.read(f'{linarg_dir}/{f}/linear_arg.npz', f'{linarg_dir}/{f}/linear_arg.pvar', f'{linarg_dir}/{f}/linear_arg.psam')   
linarg = linarg.make_triangular() 

N = int(linarg.shape[0] / 2)
M = int(linarg.shape[1])

data = np.ones(2*N)
row_indices = np.repeat(np.arange(N), 2)
col_indices = np.arange(2*N)
S = sp.csr_matrix((data, (row_indices, col_indices)), shape=(N, 2*N))

np.random.seed(42)
y = np.random.normal(0, 1, N)

start = time.time()
xTy = ((y @ S) @ linarg) [0]
allele_counts =  ((np.ones(N) @ S) @ linarg) [0]
xTx = 2 / N * allele_counts * (N - allele_counts) # 2Npq
effect_sizes_linarg = xTy / xTx
end = time.time()

with open(f'{res_dir}/linarg_lin_reg_stats.txt', 'w') as file:
    file.write(" ".join(['n', 'm', 'time'])+'\n')
    file.write(" ".join([str(N), str(M), str(np.round(end-start, 3))])+'\n')