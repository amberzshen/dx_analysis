from cyvcf2 import VCF
import numpy as np
import scipy.sparse
import argparse

def vcf_to_csc(region: str, out_prefix: str, phased: bool = False, flip_minor_alleles: bool = True):
    """
    Codes unphased genotypes as 0/1/2/3, where 3 means that at least one of the two alleles is unknown.
    Codes phased genotypes as 0/1, and there are 2n rows, where rows 2*k and 2*k+1 correspond to individual k.
    """
    chrom = region.split('chr')[1].split(':')[0]
    vcf_file=f'/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c{chrom}_b0_v1.vcf.gz'
    vcf = VCF(vcf_file, gts012=True, strict_gt=True)
    vcf_region = vcf(region)
    
    n_samples = len(vcf.samples)    
    genotype_mat = scipy.sparse.coo_matrix((n_samples, 0))
    flip = False
    
    ploidy = 1 if phased else 2
    
    variant_metadata_path = f'genotype_matrices/variant_metadata/{out_prefix}_{region}.txt'
    with open(variant_metadata_path, 'w') as f:
        f.write("##fileformat=PVARv1.0\n")
        f.write("##INFO=<ID=IDX,Number=1,Type=Integer,Description=\"Variant Index\">\n")
        f.write("##INFO=<ID=FLIP,Number=1,Type=Integer,Description=\"Flip Information\">\n")
        f.write("#CHROM POS ID REF ALT INFO\n")
    f = open(variant_metadata_path, 'a')
    var_index = 0
    # TODO: handle missing data
    for var in vcf_region:
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
        data = gts[idx]
        row = idx
        col = np.zeros(len(data))
        genotype_mat_var = scipy.sparse.coo_matrix((data, (row, col)), shape=(n_samples, 1))
        genotype_mat = scipy.sparse.hstack([genotype_mat, genotype_mat_var])    
        
        f.write(' '.join([chrom, str(var.POS), '.', var.REF, ','.join(var.ALT), f'IDX={var_index};FLIP={int(flip)}'])+'\n')
        var_index += 1
    
    f.close()    
    scipy.sparse.save_npz(f'genotype_matrices/matrices/{out_prefix}_{region}.npz', genotype_mat)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('region', type=str)
    parser.add_argument('out_prefix', type=str)
    args = parser.parse_args()
    
    vcf_to_csc(args.region, args.out_prefix, phased=True, flip_minor_alleles=False)
    

