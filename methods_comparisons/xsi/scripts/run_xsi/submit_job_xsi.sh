chrom=1
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_xsi.sh" \
    -icmd="bash run_xsi.sh $chrom" \
    --destination "/methods_comparisons/xsi/" \
    --instance-type mem3_ssd1_v2_x2 \
    --priority high \
    --name "xsi_chr${chrom}" \
    --extra-args '{"timeoutPolicy": {"*": {"hours": 504}}}' \
    --brief \
    -y

chrom=11
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_xsi.sh" \
    -icmd="bash run_xsi.sh $chrom" \
    --destination "/methods_comparisons/xsi/" \
    --instance-type mem3_ssd1_v2_x2 \
    --priority high \
    --name "xsi_chr${chrom}" \
    --extra-args '{"timeoutPolicy": {"*": {"hours": 504}}}' \
    --brief \
    -y