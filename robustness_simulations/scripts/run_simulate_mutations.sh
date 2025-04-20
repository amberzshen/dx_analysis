#!/bin/bash
#SBATCH -n 1
#SBATCH -t 3-00:00:00
#SBATCH -p medium
#SBATCH --mem=32GB
#SBATCH --output=/n/data1/hms/dbmi/oconnor/lab/amber/slurm/250130_sim_muts_%a.out
#SBATCH --error=/n/data1/hms/dbmi/oconnor/lab/amber/slurm/250130_sim_muts_%a.err
#SBATCH --job-name="sim_muts"
#SBATCH --array=1-358
#SBATCH --mail-user amber_shen@g.harvard.edu
#SBATCH --mail-type=ALL

params="../params/ooa_updated2_params.csv"
n_muts=$(awk -F',' 'NR==i {print $j}' i=$SLURM_ARRAY_TASK_ID j=1 $params)
simulation_name=$(awk -F',' 'NR==i {print $j}' i=$SLURM_ARRAY_TASK_ID j=2 $params)

python simulate_mutations.py \
        $n_muts \
        "/n/data1/hms/dbmi/oconnor/lab/amber/msprime_simulations/simulated_tree_sequences/" \
        "/n/data1/hms/dbmi/oconnor/lab/amber/msprime_simulations/simulated_genotype_matrices/" \
        $simulation_name \
        "/n/data1/hms/dbmi/oconnor/lab/amber/simulate_mutations/simulated_tree_sequences_w_simulated_mutations/"
