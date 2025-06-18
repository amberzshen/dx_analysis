import polars as pl
import os
import numpy as np

covariates_path = '/mnt/project/phenotypes/age_sex_height_pcs.csv'
phenotypes_path = '/mnt/project/phenotypes/phenotypes_raw_20250530.csv'
whitelist_path = '/mnt/project/sample_metadata/ukb20279/250129_whitelist.txt'

with open(whitelist_path, 'r') as f:
    whitelist = np.array([int(line.strip()) for line in f], dtype=np.int64)

covariates = pl.read_csv(covariates_path)
covariates = covariates.filter(pl.col('eid').is_in(whitelist))
covariates = covariates.with_columns(pl.lit(1).alias("intercept"))
covariates = covariates.rename({"eid": "IID"})
covariates = covariates.with_columns(
    pl.when(pl.col("p31") == "Male").then(1).otherwise(0).alias("p31")
)

covariate_ids = ['intercept', 'p21022', 'p31'] + [f'p22009_a{i}' for i in range(1, 41)]
for col in covariate_ids:
    mean = covariates[col].mean()
    std_dev = covariates[col].std()
    
    covariates = covariates.with_columns(
        ((pl.col(col) - mean) / std_dev).alias(col)
    )

covariates = covariates.with_columns(pl.col("IID").alias("FID"))
covariates.select(["FID", "IID"] + covariate_ids).write_csv("covariates.txt", separator=" ", null_value='NA')


phenotypes = pl.read_csv('/mnt/project/phenotypes/phenotypes_raw_20250530.csv')
phenotypes = phenotypes.filter(pl.col("eid").is_in(whitelist))
phenotypes = phenotypes.rename({"eid": "IID"})
numeric_types = {pl.Int8, pl.Int16, pl.Int32, pl.Int64,
                 pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64,
                 pl.Float32, pl.Float64}
numeric_cols = [col for col, dtype in zip(phenotypes.columns, phenotypes.dtypes)
                if dtype in numeric_types]
phenotypes = phenotypes.select(numeric_cols)
n_rows = phenotypes.height
fraction_missing = phenotypes.select([
    (pl.col(col).is_null().sum() / n_rows).alias(col)
    for col in phenotypes.columns
])
high_missing_cols = [
    col for col in fraction_missing.columns
    if fraction_missing.select(pl.col(col)).item() > 0.8
]
phenotypes = phenotypes.drop(high_missing_cols)

phenotype_ids = phenotypes.columns[1:] # ignore IID
for col in phenotype_ids:
    mean = phenotypes[col].mean()
    std_dev = phenotypes[col].std()
    
    phenotypes = phenotypes.with_columns(
        ((pl.col(col) - mean) / std_dev).alias(col)
    )
phenotypes = phenotypes.with_columns(pl.col("IID").alias("FID"))
phenotypes.select(["FID", "IID"] + phenotype_ids).write_csv("phenotypes.txt", separator=" ", null_value='NA')
