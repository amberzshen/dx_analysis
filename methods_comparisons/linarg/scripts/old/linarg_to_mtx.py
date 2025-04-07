import linear_dag as ld

linarg_path = '/mnt/project/linear_args/ukb20279/chr21/0_chr21-5030618-25863389/linear_arg'
save_path = '0_chr21-5030618-25863389_julia'
linarg = ld.LinearARG.read(f'{linarg_path}.npz', f'{linarg_path}.pvar.gz', f'{linarg_path}.psam.gz')
linarg.write(save_path, format="mtx")

linarg_path = '/mnt/project/linear_args/ukb20279/chr21/1_chr21-25863390-46696162/linear_arg'
save_path = '1_chr21-25863390-46696162_julia'
linarg = ld.LinearARG.read(f'{linarg_path}.npz', f'{linarg_path}.pvar.gz', f'{linarg_path}.psam.gz')
linarg.write(save_path, format="mtx")
