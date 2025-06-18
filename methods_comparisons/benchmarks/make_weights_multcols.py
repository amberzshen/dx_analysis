import h5py
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("chrom", type=str)
parser.add_argument("NUM_WEIGHTS", type=int)
args = parser.parse_args()

# linarg_dir = f'/mnt/project/linear_args/ukb20279/chr{args.chrom}'

# POS = []
# REF = []
# ALT = []

# for partition in os.listdir(linarg_dir):
#     with h5py.File(f'{linarg_dir}/{partition}/linear_arg.h5', 'r') as f:
#         POS += list(f['POS'][:])
#         REF += [x.decode('utf-8') for x in f['REF'][:]]
#         ALT += [x.decode('utf-8') for x in f['ALT'][:]]

# IDS = [f'{args.chrom}:{POS[i]}:{REF[i]}:{ALT[i].split(",")[0]}' for i in range(len(POS))]
# A1 = [ALT[i].split(",")[0] for i in range(len(POS))]

# # Generate 100 normally distributed weights per variant
# NUM_WEIGHTS = 100
# WEIGHTS = np.random.normal(size=(len(IDS), NUM_WEIGHTS))

# # Stack everything together: ID, A1, WEIGHT_1...WEIGHT_100
# weights_output = np.column_stack((IDS, A1, WEIGHTS))

# # Create header
# header = "ID\tA1\t" + "\t".join([f"WEIGHT_{i+1}" for i in range(NUM_WEIGHTS)])

# # Save to file
# np.savetxt("weights.txt", weights_output, fmt="%s", delimiter="\t", header=header, comments="")


linarg_dir = f'/mnt/project/linear_args/ukb20279/chr{args.chrom}'

output_path = f"weights_{args.NUM_WEIGHTS}.txt"

with open(output_path, "w") as out_f:
    # Write header
    header = "ID\tA1\t" + "\t".join([f"WEIGHT_{i+1}" for i in range(args.NUM_WEIGHTS)])
    out_f.write(header + "\n")

    for partition in os.listdir(linarg_dir):
        with h5py.File(f'{linarg_dir}/{partition}/linear_arg.h5', 'r') as f:
            POS = f['POS'][:]
            REF = [x.decode('utf-8') for x in f['REF'][:]]
            ALT = [x.decode('utf-8') for x in f['ALT'][:]]

            for pos, ref, alt in zip(POS, REF, ALT):
                alt1 = alt.split(",")[0]
                variant_id = f'{args.chrom}:{pos}:{ref}:{alt1}'
                weights = np.random.normal(size=args.NUM_WEIGHTS)
                weights_str = "\t".join(f"{w:.6f}" for w in weights)
                out_f.write(f"{variant_id}\t{alt1}\t{weights_str}\n")