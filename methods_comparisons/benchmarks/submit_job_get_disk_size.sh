dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_disk_size.py" \
    -iin="/amber/scripts/run_get_disk_size.sh" \
    -icmd="bash run_get_disk_size.sh" \
    --destination "/" \
    --instance-type "mem1_ssd1_v2_x2" \
    --priority high \
    --name "get_disk_size" \
    --brief \
    -y