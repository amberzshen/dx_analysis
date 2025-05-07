from scipy.sparse import csc_matrix, csr_matrix, diags, eye, load_npz, save_npz
import gzip
import numpy as np
import polars as pl
from collections import defaultdict
import os
import argparse

from linear_dag.core.lineararg import remove_degree_zero_nodes, make_triangular, LinearARG, VariantInfo
from linear_dag.core.data_structures import DiGraph
from linear_dag.core.one_summed_cy import linearize_brick_graph


def read_variant_info(path):
    
    req_fields = ["CHROM", "POS", "ID", "REF", "ALT", "INFO"]
    
    if path is None:
        raise ValueError("path argument cannot be None")

    def _parse_info(info_str):
        idx = -1
        flip = False
        for info in info_str.split(";"):
            s_info = info.split("=")
            if len(s_info) == 2 and s_info[0] == "IDX":
                idx = int(s_info[1])
            elif len(s_info) == 1 and s_info[0] == "FLIP":
                flip = True

        return idx, flip

    open_f = gzip.open if str(path).endswith(".gz") else open
    header_map = None
    var_table = defaultdict(list)
    with open_f(path, "rt") as var_file:
        for line in var_file:
            if line.startswith("##"):
                continue
            elif line[0] == "#":
                names = line[1:].strip().split()
                header_map = {key: idx for idx, key in enumerate(names)}
                for req_name in req_fields:
                    if req_name not in header_map:
                        # we check again later based on dataframe, but better to error out early when parsing
                        raise ValueError(f"Required column {req_name} not found in header table")
                continue

            # parse row; this can easily break...
            row = line.strip().split()
            for field in req_fields:
                # skip INFO for now...
                if field == "INFO":
                    continue
                value = row[header_map[field]]
                var_table[field].append(value)

            # parse info to pull index and flip info if they exist
            idx, flip = _parse_info(row[header_map["INFO"]])
            var_table['IDX'].append(idx)
            var_table['FLIP'].append(flip)

    var_table = pl.DataFrame(var_table)
    return var_table


def read_old_linear_arg(matrix_fname):
    
    variant_fname = matrix_fname[:-4] + ".pvar.gz"
    samples_fname = matrix_fname[:-4] + ".psam.gz"
    
    sample_info = pl.read_csv(samples_fname, separator=" ")
    sample_indices = np.array(sample_info["IDX"])
    
    var_table = read_variant_info(variant_fname)
    
    A = csc_matrix(load_npz(matrix_fname)) # convert from csr to csc
    
    return A, sample_indices, var_table



def remove_duplicate_variants(var_table, start, end):
    """
    simply remove the duplicate variants indices and do not change the graph. may hurt compression a little, but these variants are so rare
    that it likely does not matter. alternatively, all node children and parents need to be connected with edge weight equal to the product of 
    the edge weight of the child and parent.
    """
    
    var_table = var_table.with_columns(pl.col("POS").cast(pl.Int64))
    var_table = var_table.with_row_index(name="row_idx")
    var_table = var_table.with_columns(pl.concat_str(["ID", "REF", "ALT"], separator="-").alias("unique_identifier"))
        
    large_partition_filt = var_table.filter((pl.col("POS") >= start) & (pl.col("POS") <= end))
    small_partition_filt = var_table.unique(subset=["unique_identifier"], keep="first")
    
    var_table_filt = large_partition_filt.join(small_partition_filt, on=large_partition_filt.columns, how="inner")
    
    indices_to_keep = var_table_filt["row_idx"].to_list()
    
    return var_table_filt, indices_to_keep


def convert_to_new_format(matrix_fname):
    
    print('reading in old linear ARG...', flush=True)
    A, sample_indices, var_table = read_old_linear_arg(matrix_fname)
    n_variants = var_table.height
    
    print('removing indels...', flush=True)
    start = int(matrix_fname.split('/')[-2].split('-')[1])
    end = int(matrix_fname.split('/')[-2].split('-')[2])
    
    var_table, indices_to_keep = remove_duplicate_variants(var_table, start, end)
    print(f'removed {n_variants - var_table.height} indels')
    
    var_info = var_table.drop(["IDX", "FLIP"])
    variant_indices = np.array(var_table.get_column("IDX").to_list())
    flip = np.array(var_table.get_column("FLIP").to_list())
        
    print('removing degree 0 nodes...', flush=True)
    A, variant_indices, sample_indices = remove_degree_zero_nodes(A, variant_indices, sample_indices)
    
    print('triangularizing...', flush=True)
    A, variant_indices = make_triangular(A, variant_indices, sample_indices)
    
    linarg = LinearARG(A, variant_indices, flip, len(sample_indices), variants=VariantInfo(var_info))
    print('computing nonunique indices...', flush=True)
    linarg.calculate_nonunique_indices()
    
    print(f'number of variants before: {n_variants}, number of variants after: {len(variant_indices)}')
    return linarg, indices_to_keep


def check_allele_counts(linarg_dir, load_dir, indices_to_keep):
    """
    Get stats from linear ARG.
    """
    genotypes_dir = f'{load_dir}/{args.linarg_dir}genotype_matrices/'
    
    linarg = LinearARG.read(f"{linarg_dir}/linear_arg.h5")
    linarg.flip = np.array([False for i in range(linarg.shape[1])])

    v = np.ones(linarg.shape[0])
    allele_counts_from_linarg = v @ linarg

    files = os.listdir(f"{genotypes_dir}")
    ind_arr = np.array([int(f.split("_")[0]) for f in files])
    order = ind_arr.argsort()
    files = np.array(files)[order].tolist()  # sort files by index
    genotypes_nnz = 0
    allele_counts = []
    for f in files:
        
        genotypes = load_npz(f"{genotypes_dir}/{f}")
        
        # with h5py.File(f"{load_dir}{linarg_dir}/genotype_matrices/{f}", 'r') as f:
        #     genotypes = sp.csc_matrix((f['data'][:], f['indices'][:], f['indptr'][:]), shape=f['shape'][:]) 
            
        v_0 = np.ones(genotypes.shape[0])
        allele_count_from_genotypes = v_0 @ genotypes
        allele_counts.append(allele_count_from_genotypes)
    allele_counts_from_genotype = np.concatenate(allele_counts)
    allele_counts_from_genotype = allele_counts_from_genotype[indices_to_keep]

    correct = all(allele_counts_from_genotype == allele_counts_from_linarg)
    print(f'allele counts match: {correct}', flush=True)
    return correct
  
  


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('linarg_dir', type=str)
    args = parser.parse_args()
        
    load_dir = '/mnt/project'
        
    linarg, indices_to_keep = convert_to_new_format(f'{load_dir}/{args.linarg_dir}linear_arg.npz')
    os.makedirs(args.linarg_dir, exist_ok=True)
    linarg.write(f'{args.linarg_dir}linear_arg')
    
    correct = check_allele_counts(args.linarg_dir, load_dir, indices_to_keep)
    if not correct:
        os.remove(f'{args.linarg_dir}linear_arg.h5')
        raise ValueError("converted linear ARG not correct. file deleted.")



    


