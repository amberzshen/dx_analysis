instance_type="mem3_ssd1_v2_x4" # 32GB

# parition 0
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_benchmark_h5_dot_product.sh" \
    -iin="/amber/scripts/benchmark_h5_dot_product.py" \
    -iin="/amber/test_npz_to_h5/linear_arg.h5" \
    -iin="/amber/test_npz_to_h5/linear_arg.pvar.gz" \
    -iin="/amber/test_npz_to_h5/linear_arg.psam.gz" \
    -icmd="bash run_benchmark_h5_dot_product.sh" \
    --destination "/" \
    --instance-type $instance_type \
    --priority high \
    --name "0_h5_dot_product" \
    --brief \
    -y