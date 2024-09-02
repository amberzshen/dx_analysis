import linear_dag as ld
from linear_dag.brick_graph import merge_brick_graphs
from linear_dag.one_summed_cy import linearize_brick_graph
import polars as pl
import argparse
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument('run_identifier', type=str)
args = parser.parse_args()

merged_graph, variant_indices, num_samples, index_mapping = merge_brick_graphs(f'/mnt/project/linear_arg_results/{args.run_identifier}/brick_graph_partitions')
merged_graph_recom = ld.Recombination.from_graph(merged_graph)
merged_graph_recom.find_recombinations()
linear_arg_adjacency_matrix = linearize_brick_graph(merged_graph_recom)
sample_idx = np.arange(num_samples)

# get VariantInfo
files = os.listdir(f'/mnt/project/linear_arg_results/{args.run_identifier}/variant_metadata/')
ind_arr = np.array([int(f.split('_')[0]) for f in files])
order = ind_arr.argsort()
files = np.array(files)[order].tolist() # sort files by index
df_list = [pl.read_csv(f'{linarg_dir}/variant_metadata/{f}', separator=' ') for f in files]
df = pl.concat(df_list)
df.with_column((variant_indices).alias('IDX')) # replace old indices with new merged ones
var_info = ld.VariantInfo(df)

linarg = ld.LinearARG(linear_arg_adjacency_matrix, sample_idx, var_info)
linarg.write(f'{args.run_identifier}/linear_arg')

