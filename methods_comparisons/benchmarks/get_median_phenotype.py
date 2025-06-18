import pandas as pd

df = pd.read_csv('/mnt/project/phenotypes/phenotypes_raw_20250617.csv')
non_array_phenos = [x for x in list(df.columns) if len(x.split('_'))<3]
phenos = list(set([x.split('_')[0] for x in non_array_phenos[1:]]))

for pheno in phenos:
    instances = [x for x in non_array_phenos if pheno in x]
    df[pheno] = df[instances].select_dtypes(include='number').median(axis=1)
    
df = df[phenos]
df.to_csv('phenotypes_median_20250617.csv', index=False)