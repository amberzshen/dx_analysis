import h5py
import linear_dag as ld
import gzip

linarg = ld.LinearARG.read('/mnt/project/linear_args/ukb20279/chr21/0_chr21-5030618-25863389/linear_arg.npz')
prefix = 'linear_arg'

# write out samples
iids = None
with gzip.open(f"{prefix}.psam.gz", "wt") as f_samples:
    f_samples.write("#IID IDX\n")
    if iids is None:
        iids = [f"sample_{idx}" for idx in range(linarg.shape[0])]
    for i, iid in enumerate(iids):
        f_samples.write(f"{iid} {linarg.sample_indices[i]}\n")

# write out variant info
linarg.variants.write(prefix + ".pvar.gz")

# write out DAG info
compression_option = 'gzip'
with h5py.File(prefix + ".h5", "w") as f:
    f.attrs['n'] = linarg.A.shape[0]
    f.create_dataset('indptr', data=linarg.A.indptr, compression=compression_option, shuffle=True)
    f.create_dataset('indices', data=linarg.A.indices, compression=compression_option, shuffle=True)
    f.create_dataset('data', data=linarg.A.data, compression=compression_option, shuffle=True)
    f.create_dataset('variant_indices', data=linarg.variant_indices, compression=compression_option, shuffle=True)
    f.create_dataset('flip', data=linarg.flip, compression=compression_option, shuffle=True)