# cat get_geno_ids.txt | xargs -P64 -I{} dx describe {}  | grep Price | tr -d '£' | awk '{sum+=$3; print sum}'

# cat forward_backward_ids.txt | xargs -P64 -I{} dx describe {}  | grep Price | tr -d '£' | awk '{sum+=$3; print sum}'

# cat reduction_ids.txt | xargs -P64 -I{} dx describe {}  | grep Price | tr -d '£' | awk '{sum+=$3; print sum}'

# cat merge_ids.txt | xargs -P64 -I{} dx describe {}  | grep Price | tr -d '£' | awk '{sum+=$3; print sum}'

# cat get_geno_chrX_ids.txt | xargs -P64 -I{} dx describe {}  | grep Price | tr -d '£' | awk '{sum+=$3; print sum}'

# cat forward_backward_chrX_ids.txt | xargs -P64 -I{} dx describe {}  | grep Price | tr -d '£' | awk '{sum+=$3; print sum}'

# cat reduction_chrX_ids.txt | xargs -P64 -I{} dx describe {}  | grep Price | tr -d '£' | awk '{sum+=$3; print sum}'

# cat merge_chrX_ids.txt | xargs -P64 -I{} dx describe {}  | grep Price | tr -d '£' | awk '{sum+=$3; print sum}'

cat add_ind_ids.txt | xargs -P64 -I{} dx describe {}  | grep Price | tr -d '£' | awk '{sum+=$3; print sum}'


