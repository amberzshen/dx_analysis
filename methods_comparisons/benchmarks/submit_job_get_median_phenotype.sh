dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_median_phenotype.py" \
    -iin="/amber/scripts/run_get_median_phenotype.sh" \
    -icmd="bash run_get_median_phenotype.sh" \
    --destination "/phenotypes/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "get_median_phenotype" \
    --brief \
    -y