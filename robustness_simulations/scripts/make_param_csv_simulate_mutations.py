import pandas as pd
import os

out = 'ooa_updated3'
n_mutation_list = [10, 50, 100, 500, 1000]
df = pd.DataFrame(columns=['n_muts', 'simulation_name'])
simulations = [f'100000_chr21-21990355-23324211_{i}' for i in range(1, 101)]

out_dir = '/n/data1/hms/dbmi/oconnor/lab/amber/simulate_mutations/simulated_tree_sequences_w_simulated_mutations/'
mut_types = ['back', 'recurrent', 'error', 'position']

for simulation_name in simulations:
    for n_muts in n_mutation_list:
        if all([os.path.exists(f'{out_dir}/{mut_type}/{simulation_name}_{n_muts}.npz') for mut_type in mut_types]):
            continue
        df.loc[df.shape[0]] = [n_muts, simulation_name]

df.to_csv(f'../params/{out}_params.csv', index=False, header=False)



# out = 'ooa'
# n_mutation_list = [0, 10, 100, 1000, 10000]
# n_replicates = 1

# df = pd.DataFrame(columns=['n_muts', 'seed', 'out'])

# for n_muts in n_mutation_list:
#     for i in range(n_replicates):
#         df.loc[df.shape[0]] = [n_muts, i, out]

# df.to_csv(f'../params/{out}_params.csv', index=False, header=False)

