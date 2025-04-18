import pygrgl
import numpy as np
import time

grg_path = 'ukb20279_c11_b0_v1_250129_whitelist.grg'
t1 = time.time()
# grg = pygrgl.load_immutable_grg(grg_path)
grg = pygrgl.load_mutable_grg(grg_path)
t2 = time.time()
y = np.random.normal(0, 10, grg.num_samples)
t3 = time.time()
b = pygrgl.dot_product(grg, y, pygrgl.TraversalDirection.UP)
t4 = time.time()

print(f'load time: {np.round(t2-t1, 3)}, dot product time: {np.round(t4-t3, 3)}')