import pygrgl
import numpy as np
from memory_profiler import memory_usage
import time
from scipy.sparse import load_npz
import polars as pl
from linear_dag import LinearARG
import os


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


def time_grg_matmat(grg_path, n_vectors):
    load_time, load_mem = benchmark(pygrgl.load_immutable_grg, grg_path, repeat=5)
    grg = pygrgl.load_immutable_grg(grg_path)
    y = np.random.normal(size=(n_vectors, grg.num_samples))
    dp_time, dp_mem = benchmark(pygrgl.matmul, grg, y, pygrgl.TraversalDirection.UP, repeat=5)
    return load_time, load_mem, dp_time, dp_mem


def time_linarg_matmat(linarg_path, n_vectors):
    load_time, load_mem = benchmark(LinearARG.read, linarg_path, repeat=5)
    linarg = LinearARG.read(linarg_path, load_metadata=False)
    y = np.random.normal(size=(n_vectors, linarg.shape[0]))
    dp_time, dp_mem = benchmark(lambda: y @ linarg, repeat=5)
    return load_time, load_mem, dp_time, dp_mem


def time_scipy_matmat(genotypes_path, n_vectors):
    load_time, load_mem = benchmark(load_npz, genotypes_path, repeat=5)
    genotypes = load_npz(genotypes_path)
    y = np.random.normal(size=(n_vectors, genotypes.shape[0]))
    dp_time, dp_mem = benchmark(lambda: y @ genotypes, repeat=5)
    return load_time, load_mem, dp_time, dp_mem

    
if __name__ == "__main__":
    
    results = []
    
    for n_vectors in [1, 2, 10, 100, 1000]:
        for chrom in [21]:
        
            grg_path = f'/mnt/project/methods_comparisons/grg/ukb20279_c{chrom}_b0_v1_250129_whitelist.grg'
            load_time, load_mem, dp_time, dp_mem = time_grg_matmat(grg_path, n_vectors)
            results.append((chrom, 'n_vectors', 'grg', load_time, load_mem, dp_time, dp_mem))
            
            linarg_dir = f'/mnt/project/linear_args/ukb20279/chr{chrom}/'
            for partition in os.listdir(linarg_dir):
                linarg_path = f'{linarg_dir}{partition}/linear_arg.h5'
                load_time, load_mem, dp_time, dp_mem = time_linarg_matmat(linarg_path, n_vectors)
                results.append((chrom, 'n_vectors', f'linarg_{partition}', load_time, load_mem, dp_time, dp_mem))
                
            for large_partition in os.listdir(linarg_dir):
                for file in os.listdir(f'{linarg_dir}/{large_partition}/genotype_matrices/'):
                    genotypes_path = f'{linarg_dir}/{large_partition}/genotype_matrices/{file}'
                    load_time, load_mem, dp_time, dp_mem = time_scipy_matmat(genotypes_path, n_vectors)
                    results.append((chrom, 'n_vectors', f'genotypes_{file}', load_time, load_mem, dp_time, dp_mem))
        
    df = pl.DataFrame(
        results,
        schema=["chr", "n_vectors", "method", "load_time (s)", "load_memory (MB)", "matmat_time (s)", "matmat_memory (MB)"]
    )
    
    os.makedirs("amber/methods_comparisons/results/", exist_ok=True)
    df.write_csv("amber/methods_comparisons/results/matmat_test.csv")