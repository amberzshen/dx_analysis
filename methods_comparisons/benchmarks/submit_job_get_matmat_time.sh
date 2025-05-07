dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_matmat_time.py" \
    -iin="/amber/scripts/run_get_matmat_time.sh" \
    -icmd="bash run_get_matmat_time.sh" \
    --destination "/" \
    --instance-type "mem3_ssd1_v2_x16" \
    --priority high \
    --name "matmat_time" \
    --brief \
    -y