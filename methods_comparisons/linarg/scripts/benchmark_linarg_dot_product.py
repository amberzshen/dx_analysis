import numpy as np
import time
import linear_dag as ld

t1 = time.time()
linarg = ld.LinearARG.read(f'linear_arg.npz', f'linear_arg.pvar.gz', f'linear_arg.psam.gz')
t2 = time.time()

v = np.ones(linarg.shape[0])
t3 = time.time()
allele_count_from_linarg = v @ linarg
t4 = time.time()

print(f'time to load linear ARG: {np.round(t2 - t1, 3)} seconds')
print(f'time to compute dot product: {np.round(t4 - t3, 3)} seconds')
