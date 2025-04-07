import linear_dag as ld
import os

# linarg_path = '/mnt/project/1kg/1kg_chr1'
# save_path = '1kg_chr1_julia'
# linarg = ld.LinearARG.read(f'{linarg_path}.npz', f'{linarg_path}.pvar', f'{linarg_path}.psam')
# linarg.write(save_path, format="mtx")

linarg_path = '/mnt/project/1kg/1kg_chr1'
save_path = '1kg_chr1_julia'
linarg = ld.LinearARG.read(f'{linarg_path}.npz', f'{linarg_path}.pvar', f'{linarg_path}.psam')
linarg.write(save_path, format="mtx")

