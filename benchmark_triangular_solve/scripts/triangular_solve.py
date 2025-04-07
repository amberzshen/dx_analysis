import numpy as np
import time
import linear_dag as ld

linarg_path = '/mnt/project/1kg/1kg_chr1'
# linarg_path = '/Users/ambershen/Desktop/linARG/data/1kg/linear_ARGs/1kg_chr1'

t1 = time.time()
linarg = ld.LinearARG.read(f'{linarg_path}.npz', f'{linarg_path}.pvar', f'{linarg_path}.psam')
t2 = time.time()

v = np.ones(linarg.shape[0])
t3 = time.time()
allele_count_from_linarg = v @ linarg
t4 = time.time()

print(f'time to load linear ARG: {np.round(t2 - t1, 3)} seconds')
print(f'time to compute dot product: {np.round(t4 - t3, 3)} seconds')