import numpy as np
import time
import linear_dag as ld

t1 = time.time()
linarg = ld.LinearARG.read('linear_arg.h5', load_metadata=False)
t2 = time.time()

v = np.ones(linarg.shape[0])
t3 = time.time()
allele_count_from_linarg = v @ linarg
t4 = time.time()

print(f'time to load linear ARG without metadata: {np.round(t2 - t1, 3)} seconds')
print(f'time to compute dot product without metadata: {np.round(t4 - t3, 3)} seconds')


t1 = time.time()
linarg = ld.LinearARG.read('linear_arg.h5', load_metadata=True)
t2 = time.time()

v = np.ones(linarg.shape[0])
t3 = time.time()
allele_count_from_linarg = v @ linarg
t4 = time.time()

print(f'time to load linear ARG with metadata: {np.round(t2 - t1, 3)} seconds')
print(f'time to compute dot product with metadata: {np.round(t4 - t3, 3)} seconds')
