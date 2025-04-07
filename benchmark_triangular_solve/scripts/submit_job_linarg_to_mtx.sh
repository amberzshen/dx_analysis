instance_type="mem3_ssd1_v2_x2" # 16GB
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_linarg_to_mtx.sh" \
    -iin="/amber/scripts/linarg_to_mtx.py" \
    -icmd="bash run_linarg_to_mtx.sh" \
    --destination "/1kg/" \
    --instance-type $instance_type \
    --priority high \
    --name "linarg_to_mtx" \
    --brief \
    -y
