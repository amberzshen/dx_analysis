import linear_dag as ld
from linear_dag.brick_graph import merge_brick_graphs
from linear_dag.one_summed_cy import linearize_brick_graph
import argparse
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument('data_identifier', type=str)
args = parser.parse_args()

merged_graph, variant_indices, num_samples, index_mapping = merge_brick_graphs(f'/mnt/project/linear_arg_results/{args.data_identifier}/linear_arg_partitions')
linear_arg_adjacency_matrix = linearize_brick_graph(merged_graph)
variants_flipped_ref_alt = np.zeros(len(variant_indices), dtype=bool) # may have to change this eventually
sample_idx = np.arange(num_samples)
linarg = ld.LinearARG(linear_arg_adjacency_matrix, sample_idx, variant_indices, variants_flipped_ref_alt)

files = os.listdir(f'/mnt/project/linear_arg_results/{args.data_identifier}/variant_metadata/')
ind_arr = np.array([int(f.split('_')[0]) for f in files])
order = ind_arr.argsort()
files = np.array(files)[order].tolist() # sort files by index

positions = []
refs = []
alts = []
for var_meta in files:
    with open(f'/mnt/project/linear_arg_results/{args.data_identifier}/variant_metadata/{var_meta}', 'r') as f:
        lines = f.readlines()[4:] # skip header lines
        for line in lines:
            items = line.split()
            positions.append(items[1])
            refs.append(items[3])
            alts.append(items[4])

print(len(positions))
print(linarg.shape)

chrom = args.data_identifier.split('_')[1].split('chr')[1].split('-')[0]
linarg.write(f'{args.data_identifier}/linear_arg', chrom, positions, refs, alts,
             sample_filename=f'{args.data_identifier}/linear_arg')

