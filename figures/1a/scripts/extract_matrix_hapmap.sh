data_path="/Users/ambershen/Desktop/linARG/data/hapmap3_r1_b36_fwd.qc.poly/hapmap3_r1_b36_fwd.CEU.qc.poly.recode"
mtx="/Users/ambershen/Desktop/linARG/dx_analysis/figures/1a/data/hapmap3_CEU_chr2-234876004-234884481"
out="/Users/ambershen/Desktop/linARG/dx_analysis/figures/1a/data/hapmap3_CEU_chr2-234876004-234884481.txt"


/Users/ambershen/Desktop/software/plink1.9/plink --file $data_path \
    --chr 2 \
    --from-bp 234876004 \
    --to-bp 234884481 \
    --recode A \
    --out $mtx

tail -n +2 "${mtx}.raw" | cut -d' ' -f7- > $out