dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_size_in_memory.py" \
    -iin="/amber/scripts/run_get_size_in_memory.sh" \
    -icmd="bash run_get_size_in_memory.sh" \
    --destination "/" \
    --instance-type "mem3_ssd1_v2_x8" \
    --priority high \
    --name "get_size_in_memory" \
    --brief \
    -y