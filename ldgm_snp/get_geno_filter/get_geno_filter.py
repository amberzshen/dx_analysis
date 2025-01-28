import numpy as np
from cyvcf2 import VCF
import scipy.sparse
import pandas as pd
import os
import argparse


def make_genotype_matrix(vcf_path, linarg_dir, region, partition_number, phased=True, flip_minor_alleles=False):
    """
    From vcf file, saves the genotype matrix as csc sparse matrix, variant metadata, and filtered out variants.
    Codes unphased genotypes as 0/1/2/3, where 3 means that at least one of the two alleles is unknown.
    Codes phased genotypes as 0/1, and there are 2n rows, where rows 2*k and 2*k+1 correspond to individual k.
    """
    if not os.path.exists(f"{linarg_dir}/variant_metadata/"):
        os.makedirs(f"{linarg_dir}/variant_metadata/")
    if not os.path.exists(f"{linarg_dir}/genotype_matrices/"):
        os.makedirs(f"{linarg_dir}/genotype_matrices/")

    chrom = region.split("chr")[1].split("-")[0]
    start = int(region.split("-")[1])
    end = int(region.split("-")[2])
    region_formatted = f'{region.split("-")[0]}:{region.split("-")[1]}-{region.split("-")[2]}'
    vcf = VCF(vcf_path, gts012=True, strict_gt=True)
    
    snplist_dir = '/mnt/project/ldgm_snps/'
    snplists = [x for x in os.listdir(snplist_dir) if (x.split('_')[1].split('chr')[1]==chrom) and (int(x.split('_')[3].split('.')[0])>=start) and (int(x.split('_')[2])<=end)]
    ind_arr = np.array([int(s.split('_')[2]) for s in snplists])
    order = ind_arr.argsort()
    snplists = np.array(snplists)[order].tolist()  # sort files by index
    dfs = [pd.read_csv(f'{snplist_dir}{s}') for s in snplists] 
    df = pd.concat(dfs, ignore_index=True)
    df = df[(df.position>=start) & (df.position<=end)]
    snps = {r.position: [r.anc_alleles, r.deriv_alleles] for _,r in df.iterrows()}

    data = []
    idxs = []
    ptrs = [0]
    flip = False
    ploidy = 1 if phased else 2

    f_var = open(f"{linarg_dir}/variant_metadata/{partition_number}_{region}.txt", "w")
    f_var.write(" ".join(["CHROM", "POS", "ID", "REF", "ALT", "FLIP", "IDX"]) + "\n")

    var_index = 0
    for var in vcf(region_formatted):
        
        if var.POS in snps:
            if (var.REF not in snps[var.POS]) or (var.ALT[0] not in snps[var.POS]): # different SNP
                continue
        else: # not in snps
            continue
        
        
        if (var.POS < start) or (var.POS > end):
            continue  # ignore indels that are outside of region
        if phased:
            gts = np.ravel(np.asarray(var.genotype.array())[:, :2])
        else:
            gts = var.gt_types
        if flip_minor_alleles:
            af = np.mean(gts) / ploidy
            if af > 0.5:
                gts = ploidy - gts
                flip = True
            else:
                flip = False

        af = np.mean(gts) / ploidy

        (idx,) = np.where(gts != 0)
        data.append(gts[idx])
        idxs.append(idx)
        ptrs.append(ptrs[-1] + len(idx))
        f_var.write(
            " ".join([chrom, str(var.POS), ".", var.REF, ",".join(var.ALT), str(int(flip)), str(var_index)]) + "\n"
        )
        var_index += 1

    f_var.close()

    data = np.concatenate(data)
    idxs = np.concatenate(idxs)
    ptrs = np.array(ptrs)
    genotypes = scipy.sparse.csc_matrix((data, idxs, ptrs), shape=(gts.shape[0], len(ptrs) - 1))

    scipy.sparse.save_npz(f"{linarg_dir}/genotype_matrices/{partition_number}_{region}.npz", genotypes)
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('vcf_path', type=str)
    parser.add_argument('linarg_dir', type=str)
    parser.add_argument('region', type=str)
    parser.add_argument('partition_number', type=str)
    args = parser.parse_args()
    
    make_genotype_matrix(args.vcf_path, args.linarg_dir, args.region, args.partition_number)