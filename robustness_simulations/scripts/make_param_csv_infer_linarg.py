import pandas as pd

out = 'ooa'
simulations = [f'100000_chr21-21990355-23324211_{i}' for i in range(1, 101)]
mutation_types = ['back', 'recurrent', 'error', 'position']
n_mutation_list = [10, 50, 100, 500, 1000]

df = pd.DataFrame(columns=['simulation_name', 'mut_type', 'n_muts'])
for simulation_name in simulations:
    for mut_type in mutation_types:
        for n_muts in n_mutation_list:
            df.loc[df.shape[0]] = [simulation_name, mut_type, n_muts]

df.to_csv(f'../params/{out}_infer_linarg_params.csv', index=False, header=False)



# out = 'ooa'
# n_mutation_list = [0, 10, 100, 1000, 10000]
# n_replicates = 1

# df = pd.DataFrame(columns=['n_muts', 'seed', 'out'])

# for n_muts in n_mutation_list:
#     for i in range(n_replicates):
#         df.loc[df.shape[0]] = [n_muts, i, out]

# df.to_csv(f'../params/{out}_params.csv', index=False, header=False)

