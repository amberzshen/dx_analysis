import pygrgl
import numpy as np
from memory_profiler import memory_usage
import time
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


def time_grg_dot_product(grg_path):
    load_time, load_mem = benchmark(pygrgl.load_immutable_grg, grg_path, repeat=10)
    grg = pygrgl.load_immutable_grg(grg_path)
    y = np.ones(grg.num_samples)
    dp_time, dp_mem = benchmark(pygrgl.matmul, grg, y, pygrgl.TraversalDirection.UP, repeat=10)
    return load_time, load_mem, dp_time, dp_mem
    

if __name__ == "__main__":
    
    results = []
        
    for chrom in [1, 11, 21]:
    
        grg_path = f'/mnt/project/methods_comparisons/grg/ukb20279_c{chrom}_b0_v1_250129_whitelist.grg'
        load_time, load_mem, dp_time, dp_mem = time_grg_dot_product(grg_path)
        results.append((chrom, 'grg', load_time, load_mem, dp_time, dp_mem))

        
    df = pl.DataFrame(
        results,
        schema=["chr", "method", "load_time (s)", "load_memory (MB)", "dot_product_time (s)", "dot_product_memory (MB)"]
    )
    
    os.makedirs("amber/methods_comparisons/results/", exist_ok=True)
    df.write_csv("amber/methods_comparisons/results/dot_product_time_grg_matmul.csv")