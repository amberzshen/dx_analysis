import polars as pl
import os
import numpy as np
import time
from memory_profiler import memory_usage
import argparse
import linear_dag as ld
from linear_dag.association.gwas import run_gwas


def benchmark(func, *args, repeat=1, interval=0.001, **kwargs):
    """
    Benchmarks a function for execution time and peak memory usage over multiple runs.

    Parameters:
        func (callable): Function to benchmark.
        *args: Positional arguments for the function.
        repeat (int): Number of times to repeat the benchmark.
        interval (float): Sampling interval for memory_profiler.
        **kwargs: Keyword arguments for the function.
    """
    total_time = 0.0
    peak_memories = []
    result = None

    for _ in range(repeat):
        start_time = time.perf_counter()

        mem_usage, result = memory_usage(
            (func, args, kwargs),
            retval=True,
            interval=interval,
            timeout=None,
            include_children=True,
            max_usage=True
        )

        end_time = time.perf_counter()

        total_time += (end_time - start_time)
        peak_memories.append(mem_usage)
        
    mean_time = total_time / repeat # seconds
    mean_peak_mem = sum(peak_memories) / repeat # MB

    return mean_time, mean_peak_mem


def time_linarg_gwas(linarg_path, iids, phenotypes, phenotype, covariates):
    
    load_time, load_mem = benchmark(ld.LinearARG.read, linarg_path, repeat=1)
    linarg = ld.LinearARG.read(linarg_path)
    linarg.iids = iids    
    gwas_time, gwas_mem = benchmark(run_gwas, linarg, phenotypes, phenotype, covariates, assume_hwe=False)

    return load_time, load_mem, gwas_time, gwas_mem


def get_phenotypes():
    
    phenotypes_path = '/mnt/project/phenotypes/age_sex_height_pcs.csv'
    whitelist_path = '/mnt/project/sample_metadata/ukb20279/250129_whitelist.txt'

    phenotypes = pl.read_csv(phenotypes_path)

    with open(whitelist_path, 'r') as f:
        whitelist = np.array([int(line.strip()) for line in f], dtype=np.int64)
    iids = pl.Series("whitelist", np.repeat(whitelist, 2)).cast(pl.Int64)
        
    phenotypes_filt = phenotypes.filter(pl.col('eid').is_in(whitelist))
    phenotypes_filt = phenotypes_filt.with_columns(pl.lit(1).alias("intercept"))
    phenotypes_filt = phenotypes_filt.rename({"eid": "iid"})
    phenotypes_filt = phenotypes_filt.with_columns(
            pl.when(pl.col("p31") == "Male").then(1).otherwise(0).alias("p31")
    )
    
    print(f'n rows before filt: {phenotypes_filt.height}')
    all_columns = ['p50_i0', 'p21022', 'p31'] + [f'p22009_a{i}' for i in range(1, 41)]
    phenotypes_filt = phenotypes_filt.drop_nulls(subset=all_columns)
    print(f'n rows after filt: {phenotypes_filt.height}')

    # standardize
    for col in all_columns:
        mean = phenotypes_filt[col].mean()
        std_dev = phenotypes_filt[col].std()
        
        phenotypes_filt = phenotypes_filt.with_columns(
            ((pl.col(col) - mean) / std_dev).alias(col)
        )
                
    phenotype = ['p50_i0']
    covariates = ['intercept', 'p21022', 'p31'] + [f'p22009_a{i}' for i in range(1, 41)]
    
    return phenotypes_filt.lazy(), phenotype, covariates, iids


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("chrom", type=str)
    args = parser.parse_args()

    phenotypes, phenotype, covariates, iids = get_phenotypes()

    linarg_dir = f'/mnt/project/linear_args/ukb20279/chr{args.chrom}'

    files = os.listdir(f'{linarg_dir}')
    ind_arr = np.array([int(f.split('_')[0]) for f in files])
    order = ind_arr.argsort()
    files = np.array(files)[order].tolist() # sort files by index
    
    results = []
    for f in files:
        linarg_path = f'{linarg_dir}/{f}/linear_arg_individual.h5'
        load_time, load_mem, gwas_time, gwas_mem = time_linarg_gwas(linarg_path, iids, phenotypes, phenotype, covariates)
        results.append([str(args.chrom), str(f), str(load_time), str(load_mem), str(gwas_time), str(gwas_mem)])
        
    output_path = f"linarg_chr{args.chrom}_gwas_time.csv"

    with open(output_path, "w") as f:
        # Write CSV header
        f.write("chr,partition,load_time,load_memory,gwas_time,gwas_memory\n")
        
        # Write each result row
        for row in results:
            f.write(",".join(map(str, row)) + "\n")


    # results = None
    # for f in files:
    #     linarg = ld.LinearARG.read(f'{linarg_dir}/{f}/linear_arg.h5')
    #     linarg.iids = pl.Series("whitelist", np.repeat(whitelist, 2)).cast(pl.Int64)
    #     res = run_gwas(linarg, phenotypes_filt.lazy(), phenotype, covariates).collect()
    #     if results is None:
    #         results = res
    #     else:
    #         results = pl.concat([results, res], how="vertical")
            
    # results.write_csv(f"chr{args.chrom}_height_gwas_results.csv")
