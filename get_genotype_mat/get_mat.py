from cyvcf2 import VCF
import numpy as np
import scipy.sparse
import argparse

def vcf_to_csc(region: str, out_prefix: str, phased: bool = False, flip_minor_alleles: bool = True):
    """
    Codes unphased genotypes as 0/1/2/3, where 3 means that at least one of the two alleles is unknown.
    Codes phased genotypes as 0/1, and there are 2n rows, where rows 2*k and 2*k+1 correspond to individual k.
    """
    vcf = VCF(f'tmp/{out_prefix}_{region}.bcf', gts012=True, strict_gt=True)
    chrom = region.split('chr')[1].split(':')[0]
    data = []
    idxs = []
    ptrs = [0]
    var_metadata = []
    flip = False
    
    ploidy = 1 if phased else 2

    # TODO: handle missing data
    for var in vcf:
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

        (idx,) = np.where(gts != 0)
        data.append(gts[idx])
        idxs.append(idx)
        ptrs.append(ptrs[-1] + len(idx))
        var_metadata.append(' '.join([chrom, str(var.POS), '.', var.REF, ','.join(var.ALT), f'IDX={len(var_metadata)};FLIP={int(flip)}']))
        # var_metadata.append(' '.join([str(var.POS), var.REF, ','.join(var.ALT), str(var.QUAL), str(flip)]))
        
    data = np.concatenate(data)
    idxs = np.concatenate(idxs)
    ptrs = np.array(ptrs)
    genotypes = scipy.sparse.csc_matrix((data, idxs, ptrs))
    
    scipy.sparse.save_npz(f'genotype_matrices/matrices/{out_prefix}_{region}.npz', genotypes)
    
    with open(f'genotype_matrices/variant_metadata/{out_prefix}_{region}.txt', 'w') as file:
        file.write("##fileformat=PVARv1.0\n")
        file.write("##INFO=<ID=IDX,Number=1,Type=Integer,Description=\"Variant Index\">\n")
        file.write("##INFO=<ID=FLIP,Number=1,Type=Integer,Description=\"Flip Information\">\n")
        file.write("#CHROM POS ID REF ALT INFO\n")
        for var in var_metadata:
            file.write(var + "\n")



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('region', type=str)
    parser.add_argument('out_prefix', type=str)
    args = parser.parse_args()
    
    vcf_to_csc(args.region, args.out_prefix, phased=True, flip_minor_alleles=False)
    

