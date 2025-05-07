import h5py
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("chrom", type=str)
args = parser.parse_args()
linarg_dir = f'/mnt/project/linear_args/ukb20279/chr{args.chrom}'

SNP_ID = []
ALLELE = []

for partition in os.listdir(linarg_dir):
    with h5py.File(f'{linarg_dir}/{partition}/linear_arg.h5', 'r') as f:
        SNP_ID.append(f['ID'][:])
        ALLELE.append(f['ALT'][:])
        
SNP_ID = np.concatenate(SNP_ID)
ALLELE = np.concatenate(ALLELE)
WEIGHT = np.ones(len(SNP_ID))

weights = np.column_stack((SNP_ID, ALLELE, WEIGHT))
np.savetxt("weights.txt", weights, fmt="%s", delimiter="\t", header="SNP_ID\tALLELE\tWEIGHT", comments="")