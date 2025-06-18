import polars as pl
import os
import numpy as np

phenotypes_path = '/mnt/project/phenotypes/age_sex_height_pcs.csv'
whitelist_path = '/mnt/project/sample_metadata/ukb20279/250129_whitelist.txt'

phenotypes = pl.read_csv(phenotypes_path)

with open(whitelist_path, 'r') as f:
    whitelist = np.array([int(line.strip()) for line in f], dtype=np.int64)

phenotypes_filt = phenotypes.filter(pl.col('eid').is_in(whitelist))
phenotypes_filt = phenotypes_filt.with_columns(
    pl.when(pl.col("p31") == "Male").then(1).otherwise(0).alias("p31")
)

with open("250129_whitelist_sex.txt", "w") as f:
    for item in phenotypes_filt["p31"]:
        f.write(f"{item}\n")