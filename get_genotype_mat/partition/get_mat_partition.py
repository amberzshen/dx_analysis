from cyvcf2 import VCF
import numpy as np
import scipy.sparse
import argparse

def vcf_to_csc(region: str, out_prefix: str, phased: bool = False, flip_minor_alleles: bool = True):
    """
    Codes unphased genotypes as 0/1/2/3, where 3 means that at least one of the two alleles is unknown.
    Codes phased genotypes as 0/1, and there are 2n rows, where rows 2*k and 2*k+1 correspond to individual k.
    """
    chrom = region.split('chr')[1].split('-')[0]
    region_formatted = f'{region.split("-")[0]}:{region.split("-")[1]}-{region.split("-")[2]}'
    vcf_file=f'/mnt/project/Bulk/Previous WGS releases/GATK and GraphTyper WGS/SHAPEIT Phased VCFs/ukb20279_c{chrom}_b0_v1.vcf.gz'
    vcf = VCF(vcf_file, gts012=True, strict_gt=True)
    data = []
    idxs = []
    ptrs = [0]
    flip = False
    
    ploidy = 1 if phased else 2
    
    variant_metadata_path = f'variant_metadata/{out_prefix}_{region}.txt'
    # with open(variant_metadata_path, 'w') as f:
    #     f.write("##fileformat=PVARv1.0\n")
    #     f.write("##INFO=<ID=IDX,Number=1,Type=Integer,Description=\"Variant Index\">\n")
    #     f.write("##INFO=<ID=FLIP,Number=1,Type=Integer,Description=\"Flip Information\">\n")
    #     f.write("#CHROM POS ID REF ALT INFO\n")
    # f = open(variant_metadata_path, 'a')
    f = open(variant_metadata_path, 'w')
    f.write(' '.join(['CHROM', 'POS', 'ID', 'REF', 'ALT', 'FLIP', 'IDX'])+'\n')
    var_index = 0
    # TODO: handle missing data
    for var in vcf(region_formatted):
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
        if (af == 0) or (af == 1): # filter out variants with af=0 or af=1
            # should save these to separate text file
            continue

        (idx,) = np.where(gts != 0)
        data.append(gts[idx])
        idxs.append(idx)
        ptrs.append(ptrs[-1] + len(idx))    
        # f.write(' '.join([chrom, str(var.POS), '.', var.REF, ','.join(var.ALT), f'IDX={var_index};FLIP={int(flip)}'])+'\n')
        f.write(' '.join([chrom, str(var.POS), '.', var.REF, ','.join(var.ALT), str(int(flip)), str(var_index)])+'\n')
        var_index += 1
    
    f.close()
        
    data = np.concatenate(data)
    idxs = np.concatenate(idxs)
    ptrs = np.array(ptrs)
    genotypes = scipy.sparse.csc_matrix((data, idxs, ptrs))
    
    scipy.sparse.save_npz(f'genotype_matrices/{out_prefix}_{region}.npz', genotypes)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('region', type=str)
    parser.add_argument('out_prefix', type=str)
    args = parser.parse_args()
    
    vcf_to_csc(args.region, args.out_prefix, phased=True, flip_minor_alleles=False)
    

