instance_type="mem3_ssd1_v2_x4" # 32GB

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_convert_npz_to_h5.sh" \
    -iin="/amber/scripts/convert_npz_to_h5.py" \
    -icmd="bash run_convert_npz_to_h5.sh" \
    --destination "/amber/test_npz_to_h5" \
    --instance-type $instance_type \
    --priority high \
    --name "test_convert_npz_to_h5" \
    --brief \
    -y
