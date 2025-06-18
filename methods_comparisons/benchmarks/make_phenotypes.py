import polars as pl
import os
import numpy as np

phenotypes_path = '/mnt/project/phenotypes/age_sex_height_pcs.csv'
whitelist_path = '/mnt/project/sample_metadata/ukb20279/250129_whitelist.txt'

phenotypes = pl.read_csv(phenotypes_path)

with open(whitelist_path, 'r') as f:
    whitelist = np.array([int(line.strip()) for line in f], dtype=np.int64)

phenotypes_filt = phenotypes.filter(pl.col('eid').is_in(whitelist))
phenotypes_filt = phenotypes_filt.with_columns(pl.lit(1).alias("intercept"))
phenotypes_filt = phenotypes_filt.rename({"eid": "IID"})
phenotypes_filt = phenotypes_filt.with_columns(
    pl.when(pl.col("p31") == "Male").then(1).otherwise(0).alias("p31")
)


for col in ['p50_i0', 'p21022', 'p31'] + [f'p22009_a{i}' for i in range(1,41)]:
    mean = phenotypes_filt[col].mean()
    std_dev = phenotypes_filt[col].std()
    
    phenotypes_filt = phenotypes_filt.with_columns(
        ((pl.col(col) - mean) / std_dev).alias(col)
    )

phenotype = ['p50_i0']
covariates = ['intercept', 'p21022', 'p31'] + [f'p22009_a{i}' for i in range(1, 41)]

# Add FID column (same as IID for PLINK)
phenotypes_filt = phenotypes_filt.with_columns(pl.col("IID").alias("FID"))

# Save phenotype file (FID, IID, PHENO)
phenotypes_filt.select(["FID", "IID"] + phenotype).write_csv("phenotypes.txt", separator=" ", null_value='NA')

# Save covariate file (FID, IID, covariates...)
phenotypes_filt.select(["FID", "IID"] + covariates).write_csv("covariates.txt", separator=" ", null_value='NA')
