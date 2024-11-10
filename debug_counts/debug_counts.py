import numpy as np
import scipy.sparse
import polars as pl
import argparse

from linear_dag.brick_graph import BrickGraph
from linear_dag.recombination import Recombination
from linear_dag.one_summed_cy import linearize_brick_graph
from linear_dag.lineararg import VariantInfo, LinearARG
from linear_dag.brick_graph import read_brick_graph_npz

from scipy.sparse.linalg import spsolve_triangular
from scipy.sparse import csc_matrix, csr_matrix, eye, load_npz, save_npz


def save_brick_graph(adj_mat, samples_idx, variants_idx, out):
    np.savez(out,
            brick_graph_data=adj_mat.data,
            brick_graph_indices=adj_mat.indices,
            brick_graph_indptr=adj_mat.indptr,
            brick_graph_shape=adj_mat.shape,
            sample_indices=np.array(samples_idx),
            variant_indices=np.array(variants_idx))


def get_intermediate_outputs(mtx_path, variant_path, out_dir):
    
    genotypes = scipy.sparse.load_npz(mtx_path)
    
    brick_graph, samples_idx, variants_idx = BrickGraph.from_genotypes(genotypes)
    recom = Recombination.from_graph(brick_graph)
    recom.find_recombinations()
    linear_arg_adjacency_matrix = linearize_brick_graph(recom)
    
    df = pl.read_csv(variant_path, separator=' ')
    df = df.with_columns(pl.Series(variants_idx).alias('IDX'))
    var_info = VariantInfo(df)
    
    brick_graph_adj_mat = brick_graph.to_csr()
    recom_adj_mat = recom.to_csr()
    linarg = LinearARG(linear_arg_adjacency_matrix, samples_idx, var_info)
    
    save_brick_graph(brick_graph_adj_mat, samples_idx, variants_idx, f'{out_dir}/emperical_brick_graph.npz')
    save_brick_graph(recom_adj_mat, samples_idx, variants_idx, f'{out_dir}/recom_brick_graph.npz')
    linarg.write(f'{out_dir}/linear_arg')
    
    
def placeholder_var_info(variant_indices):
    data = {}
    for col in ["IDX", "FLIP", "CHROM", "POS", "ID", "REF", "ALT", "INFO"]:
        if col == 'IDX':
            data[col] = variant_indices
        else:
            data[col] = [0]*len(variant_indices)
    return VariantInfo(pl.DataFrame(data))
    
    
# def compute_genotype_matrix(linarg_obj, start, end):
#     arrays = []
#     for i in range(start, end):
#         v = np.zeros(linarg_obj.shape[0])
#         v[i] = 1
#         arrays.append(v @ linarg_obj)
#     reconstructed_genotypes = np.vstack(arrays)
#     return reconstructed_genotypes


# def compute_genotype_matrices(res_dir, load_dir, graph_type, start, end):
#     if graph_type == 'brick_graph':
#         brick_graph, sample_indices, variant_indices = read_brick_graph_npz(np.load(f'{load_dir}{res_dir}/emperical_brick_graph.npz'))
#         brick_graph_adj_mat = brick_graph.to_csr().T.tocsr()
#         brick_graph_larg = LinearARG(brick_graph_adj_mat, sample_indices, placeholder_var_info(variant_indices))
#         brick_graph_larg = brick_graph_larg.make_triangular()
#         X_brick_graph = compute_genotype_matrix(brick_graph_larg, start, end)
#         np.save(f'{res_dir}/emperical_brick_graph_genotype_matrix_{start}-{end}.npy', X_brick_graph)
#     elif graph_type == 'recom':
#         recom, sample_indices, variant_indices = read_brick_graph_npz(np.load(f'{load_dir}{res_dir}/recom_brick_graph.npz'))
#         recom_adj_mat = recom.to_csr().T.tocsr()
#         recom_larg = LinearARG(recom_adj_mat, sample_indices, placeholder_var_info(variant_indices))
#         recom_larg = recom_larg.make_triangular()
#         X_recom = compute_genotype_matrix(recom_larg, start, end)
#         np.save(f'{res_dir}/recom_brick_graph_genotype_matrix_{start}-{end}.npy', X_recom)
#     elif graph_type == 'linarg':
#         linarg = LinearARG.read(f'{load_dir}{res_dir}/linear_arg.npz', f'{load_dir}{res_dir}/linear_arg.pvar', f'{load_dir}{res_dir}/linear_arg.psam')
#         linarg = linarg.make_triangular()
#         X_linarg = compute_genotype_matrix(linarg, start, end)
#         np.save(f'{res_dir}/linarg_genotype_matrix_{start}-{end}.npy', X_linarg)
#     else:
#         print('invalid graph type')
#         return    


def get_genotype(linarg, sample):
    # assumes a non-triangle linarg and no flipping
    non_sample_inds = set(range(linarg.A.shape[0])) - set(linarg.sample_indices)
    non_sample_inds = np.array(list(non_sample_inds))

    inds_to_keep = np.append(non_sample_inds, linarg.sample_indices[sample])
    A_subset = linarg.A[inds_to_keep[:,None], inds_to_keep]

    linarg_small = LinearARG(A_subset, np.array([len(inds_to_keep)-1]), linarg.variants)
    linarg_small = linarg_small.make_triangular()

    v = np.zeros(linarg_small.A.shape[0])
    v[linarg_small.sample_indices] = 1

    x = spsolve_triangular(eye(linarg_small.A.shape[1]) - linarg_small.A.T, v.T, lower=False)
    x = x[linarg_small.variant_indices]
    
    return x


def compute_genotype_matrix(linarg_obj, start, end):
    arrays = []
    for i in range(start, end):
        if i%100 == 0:
            print(f'{i},{np.round(i/(end-start),3)}', flush=True)
        arrays.append(get_genotype(linarg_obj, i))
    reconstructed_genotypes = np.vstack(arrays)
    return reconstructed_genotypes


def compute_genotype_matrices(res_dir, load_dir, graph_type, start, end):
    if graph_type == 'brick_graph':
        brick_graph, sample_indices, variant_indices = read_brick_graph_npz(np.load(f'{load_dir}{res_dir}/emperical_brick_graph.npz'))
        brick_graph_adj_mat = brick_graph.to_csr().T.tocsr()
        brick_graph_larg = LinearARG(brick_graph_adj_mat, sample_indices, placeholder_var_info(variant_indices))
        X_brick_graph = compute_genotype_matrix(brick_graph_larg, start, end)
        np.save(f'{res_dir}/emperical_brick_graph_genotype_matrix_{start}-{end}.npy', X_brick_graph)
    elif graph_type == 'recom':
        recom, sample_indices, variant_indices = read_brick_graph_npz(np.load(f'{load_dir}{res_dir}/recom_brick_graph.npz'))
        recom_adj_mat = recom.to_csr().T.tocsr()
        recom_larg = LinearARG(recom_adj_mat, sample_indices, placeholder_var_info(variant_indices))
        X_recom = compute_genotype_matrix(recom_larg, start, end)
        np.save(f'{res_dir}/recom_brick_graph_genotype_matrix_{start}-{end}.npy', X_recom)
    elif graph_type == 'linarg':
        linarg = LinearARG.read(f'{load_dir}{res_dir}/linear_arg.npz', f'{load_dir}{res_dir}/linear_arg.pvar', f'{load_dir}{res_dir}/linear_arg.psam')
        X_linarg = compute_genotype_matrix(linarg, start, end)
        np.save(f'{res_dir}/linarg_genotype_matrix_{start}-{end}.npy', X_linarg)
    else:
        print('invalid graph type')
        return 

    
def compute_allele_counts(res_dir, load_dir):
    
    print('starting brick graph...', flush=True)
    brick_graph, sample_indices, variant_indices = read_brick_graph_npz(np.load(f'{load_dir}{res_dir}/emperical_brick_graph.npz'))
    brick_graph_adj_mat = brick_graph.to_csr().T.tocsr()
    brick_graph_larg = LinearARG(brick_graph_adj_mat, sample_indices, placeholder_var_info(variant_indices))
    brick_graph_larg = brick_graph_larg.make_triangular()
    v = np.ones(brick_graph_larg.shape[0])
    X_brick_graph = v @ brick_graph_larg
    np.save(f'{res_dir}/emperical_brick_graph_allele_counts.npz', X_brick_graph)
    
    print('brick graph finished. starting recom...', flush=True)
    recom, sample_indices, variant_indices = read_brick_graph_npz(np.load(f'{load_dir}{res_dir}/recom_brick_graph.npz'))
    recom_adj_mat = recom.to_csr().T.tocsr()
    recom_larg = LinearARG(recom_adj_mat, sample_indices, placeholder_var_info(variant_indices))
    recom_larg = recom_larg.make_triangular()
    X_recom = v @ brick_graph_larg
    np.save(f'{res_dir}/recom_brick_graph_allele_counts.npz', X_recom)
    
    print('recom finished. starting linear ARG...', flush=True)
    linarg = LinearARG.read(f'{load_dir}{res_dir}/linear_arg.npz', f'{load_dir}{res_dir}/linear_arg.pvar', f'{load_dir}{res_dir}/linear_arg.psam')
    linarg = linarg.make_triangular()
    X_linarg = v @ brick_graph_larg
    np.save(f'{res_dir}/linarg_brick_graph_allele_counts.npz', X_linarg)
    
    print('done!', flush=True)


if __name__ == "__main__":
    
    # parser = argparse.ArgumentParser()
    # parser.add_argument('mtx_path', type=str)
    # parser.add_argument('variant_path', type=str)
    # parser.add_argument('out_dir', type=str)
    # args = parser.parse_args()
    
    # get_intermediate_outputs(args.mtx_path, args.variant_path, args.out_dir)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('res_dir', type=str)
    parser.add_argument('load_dir', type=str)
    parser.add_argument('graph_type', type=str)
    parser.add_argument('start', type=int)
    parser.add_argument('end', type=int)
    args = parser.parse_args()
    
    compute_genotype_matrices(args.res_dir, args.load_dir, args.graph_type, args.start, args.end)
    # compute_allele_counts(args.res_dir, args.load_dir)

    
    

    