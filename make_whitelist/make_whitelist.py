import numpy as np
import polars as pl

date = '250122'
sample_ids_path = '/mnt/project/sample_metadata/ukb20279/sample_ids.txt'
withdrawn_ids_path = '/mnt/project/sample_metadata/ukb20279/w86805_20241217_withdrawn_samples_application_86805.csv'

with open(sample_ids_path, "r") as f:
    sample_ids = [line.strip() for line in f]
    
with open(withdrawn_ids_path, "r") as f:
    withdrawn_ids = [line.strip() for line in f]

N = len(sample_ids)
withdrawn = np.array([True if (sample_ids[i][0]=='W' or sample_ids[i] in withdrawn_ids) else False for i in range(N)])

sample_meta = pl.DataFrame({
    'sample_index': np.arange(N),
    'sample_id': sample_ids,
    'withdrawn': withdrawn
})

whitelist = np.where(withdrawn==False)[0]

sample_meta_filtered = pl.DataFrame({
    'sample_index': np.arange(len(whitelist)),
    'sample_id': np.array(sample_ids)[whitelist].astype(int)
})

sample_meta.write_csv(f'{date}_sampleIndex_sampleID_withdrawnStatus.csv')
np.savetxt(f'{date}_sample_index_whitelist.csv', whitelist, fmt="%d")
sample_meta_filtered.write_csv(f'{date}_sampleIndex_sampleID_withdrawnRemoved.csv')
