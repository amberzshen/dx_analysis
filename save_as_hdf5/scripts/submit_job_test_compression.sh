instance_type="mem3_ssd1_v2_x2" # 16GB

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_test_compression.sh" \
    -iin="/amber/scripts/test_compression.py" \
    -iin="/linear_args/ukb20279/chr21/0_chr21-5030618-25863389/linear_arg.npz" \
    -iin="/linear_args/ukb20279/chr21/0_chr21-5030618-25863389/linear_arg.pvar.gz" \
    -iin="/linear_args/ukb20279/chr21/0_chr21-5030618-25863389/linear_arg.psam.gz" \
    -icmd="bash run_test_compression.sh" \
    --destination "/amber/" \
    --instance-type $instance_type \
    --priority high \
    --name "test_compression" \
    --brief \
    -y