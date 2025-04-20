import numpy as np
import argparse
import scipy.sparse as sp
import pandas as pd
import os
import tskit


def get_mutations(ts):
    mutations = ts.mutations()
    sites = ts.sites()
    site_positions = {site.id: site.position for site in sites}
    mutations_data = []
    for mutation in mutations:
        mutations_data.append({
            'mutation_id': mutation.id,
            'site_position': site_positions[mutation.site],
            'node': mutation.node
        })
    mutations_df = pd.DataFrame(mutations_data)
    return mutations_df


def get_descendants(sparse_matrix, node_index):
    num_nodes = sparse_matrix.shape[0]
    visited = [False] * num_nodes
    descendants = []
    def dfs(node):
        visited[node] = True
        children = sparse_matrix[node].nonzero()[1]
        for child in children:
            if not visited[child]:  # Check if the child has not been visited
                descendants.append(child)
                dfs(child)  # Recursive DFS call
    dfs(node_index)
    return descendants


def get_tree_at_site(ts, site):
    edges = pd.DataFrame({
        'left': ts.tables.edges.left,
        'right': ts.tables.edges.right,
        'parent': ts.tables.edges.parent,
        'child': ts.tables.edges.child,
    })
    nodes = set(list(edges.parent) + list(edges.child))
    N = len(nodes)
    assert N == max(nodes)+1
    edges_containing_site = edges[(edges.left<=site) & (edges.right>=site)]
    adj_mat = sp.csr_matrix((np.ones(edges_containing_site.shape[0]), (np.array(edges_containing_site.parent), np.array(edges_containing_site.child))), shape=(N, N))
    return adj_mat


def simulate_back_mutation(ts, geno_mtx, n_mutations):
    mutations = get_mutations(ts)
    for i in range(n_mutations):
        variant = np.random.choice(mutations.mutation_id)
        variant_site = mutations[mutations.mutation_id==variant].site_position.iloc[0]
        variant_node = mutations[mutations.mutation_id==variant].node.iloc[0]
        variant_tree = get_tree_at_site(ts, variant_site)
        variant_descendants = get_descendants(variant_tree, variant_node)
        if len(variant_descendants) == 0: # variant has no descendants
            continue
        back_mutation_node = np.random.choice(variant_descendants)
        descendants = set(get_descendants(variant_tree, back_mutation_node)).intersection(np.arange(geno_mtx.shape[0])) # samples with variant to flip
        if len(descendants) == 0: # no samples to flip
            continue
        for d in descendants:
            geno_mtx[d, variant] = 0
    geno_mtx.eliminate_zeros()
    return geno_mtx


def simulate_recurrent_mutation(ts, geno_mtx, n_mutations):
    mutations = get_mutations(ts)
    for i in range(n_mutations):
        variant = np.random.choice(mutations.mutation_id)
        variant_site = mutations[mutations.mutation_id==variant].site_position.iloc[0]
        variant_node = mutations[mutations.mutation_id==variant].node.iloc[0]
        variant_tree = get_tree_at_site(ts, variant_site)
        variant_ancestor_descendants = get_descendants(variant_tree, variant_node) + get_descendants(variant_tree.T, variant_node) # ancestor or descendant of variant
        nodes_in_tree = set(np.where((variant_tree.getnnz(axis=1)>0) | (variant_tree.getnnz(axis=0)>0))[0]) # individuals that are defined in the interval  
        recurrent_mutation_node_candidates = list(nodes_in_tree - set(variant_ancestor_descendants)) # nodes that are neither ancestors or descendants defined at the position
        if len(recurrent_mutation_node_candidates) == 0:
            continue
        recurrent_mutation_node = np.random.choice(recurrent_mutation_node_candidates)
        descendants = set(get_descendants(variant_tree, recurrent_mutation_node)).intersection(np.arange(geno_mtx.shape[0]))
        if len(descendants) == 0: # no samples to flip
            continue
        for d in descendants:
            geno_mtx[d, variant] = 1 # all descendants recieve recurrent mutation
    return geno_mtx


def simulate_position_switching(X, num_pairs):
    n_cols = X.shape[1]
    variant_pairs = np.random.choice(n_cols, (num_pairs, 2), replace=False)
    X_lil = X.tolil()
    for i, j in variant_pairs:
        X_lil[:, [i, j]] = X_lil[:, [j, i]]
    return X_lil.tocsc()


def simulate_genotype_error(X, n_errors):
    X_coo = X.tocoo()
    X_coo.eliminate_zeros()
    row_inds = np.random.randint(0, X_coo.shape[0], size=n_errors)
    col_inds = np.random.randint(0, X_coo.shape[1], size=n_errors)
    for i, j in zip(row_inds, col_inds):
        match = (X_coo.row == i) & (X_coo.col == j)
        if match.any(): # entry exists
            idx = np.where(match)[0][0]
            X_coo.data[idx] = 0
            X_coo.eliminate_zeros()
        else: # entry does not exist
            X_coo.row = np.append(X_coo.row, i)
            X_coo.col = np.append(X_coo.col, j)
            X_coo.data = np.append(X_coo.data, 1)
    return X_coo.tocsc()


def simulate_mutations(ts, geno_mtx, mut_type, n_muts):
    if mut_type == 'back':
        geno_mtx = simulate_back_mutation(ts, geno_mtx, n_muts)
    elif mut_type == 'recurrent':
        geno_mtx = simulate_recurrent_mutation(ts, geno_mtx, n_muts)
    elif mut_type == 'error':
        geno_mtx = simulate_genotype_error(geno_mtx, n_muts)
    elif mut_type == 'position':
        geno_mtx = simulate_position_switching(geno_mtx, n_muts)
    else:
        print('please input a valid mutation type to simulate')
        return None
    return geno_mtx


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('n_muts', type=int)
    parser.add_argument('ts_path', type=str)
    parser.add_argument('genotypes_path', type=str)
    parser.add_argument('simulation_name', type=str)
    parser.add_argument('out', type=str)
    args = parser.parse_args()
    
    ts = tskit.load(f'{args.ts_path}/{args.simulation_name}.trees')
    geno_mtx = sp.load_npz(f'{args.genotypes_path}/{args.simulation_name}.npz').T.tocsc() # results in samples x variants matrix

    for mut_type in ['back', 'recurrent', 'error', 'position']:
        if not os.path.exists(f'{args.out}/{mut_type}'): os.makedirs(f'{args.out}/{mut_type}')
        if os.path.exists(f'{args.out}/{mut_type}/{args.simulation_name}_{args.n_muts}.npz'):
            continue
        geno_mtx = simulate_mutations(ts, geno_mtx, mut_type, args.n_muts)
        sp.save_npz(f'{args.out}/{mut_type}/{args.simulation_name}_{args.n_muts}.npz', geno_mtx)
        
