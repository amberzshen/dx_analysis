import h5py
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("chrom", type=str)
args = parser.parse_args()
# linarg_dir = f'/mnt/project/linear_args/ukb20279/chr{args.chrom}'

# SNP_ID = []
# ALLELE = []

# for partition in os.listdir(linarg_dir):
#     with h5py.File(f'{linarg_dir}/{partition}/linear_arg.h5', 'r') as f:
#       SNP_ID += [x.decode('utf-8') for x in f['ID'][:]] 
#       ALLELE += [x.decode('utf-8') for x in f['ALT'][:]]

# WEIGHT = np.ones(len(SNP_ID))

# weights = np.column_stack((SNP_ID, ALLELE, WEIGHT))
# np.savetxt("weights.txt", weights, fmt="%s", delimiter="\t", header="ID\tA1\tWEIGHT", comments="")

linarg_dir = f'/mnt/project/linear_args/ukb20279/chr{args.chrom}'

POS = []
REF = []
ALT = []

for partition in os.listdir(linarg_dir):
    with h5py.File(f'{linarg_dir}/{partition}/linear_arg.h5', 'r') as f:
        POS += list(f['POS'][:])
        REF += [x.decode('utf-8') for x in f['REF'][:]]
        ALT += [x.decode('utf-8') for x in f['ALT'][:]]
        
IDS = [f'{args.chrom}:{POS[i]}:{REF[i]}:{ALT[i].split(",")[0]}' for i in range(len(POS))]
A1 = [ALT[i].split(",")[0] for i in range(len(POS))]
WEIGHT = np.ones(len(IDS))
        
weights = np.column_stack((IDS, A1, WEIGHT))
np.savetxt("weights.txt", weights, fmt="%s", delimiter="\t", header="ID\tA1\tWEIGHT", comments="")