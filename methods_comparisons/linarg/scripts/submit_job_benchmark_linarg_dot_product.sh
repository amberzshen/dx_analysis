instance_type="mem3_ssd1_v2_x4" # 32GB

# parition 0
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_benchmark_linarg_dot_product.sh" \
    -iin="/amber/scripts/benchmark_linarg_dot_product.py" \
    -iin="/linear_args/ukb20279/chr21/0_chr21-5030618-25863389/linear_arg.npz" \
    -iin="/linear_args/ukb20279/chr21/0_chr21-5030618-25863389/linear_arg.pvar.gz" \
    -iin="/linear_args/ukb20279/chr21/0_chr21-5030618-25863389/linear_arg.psam.gz" \
    -icmd="bash run_benchmark_linarg_dot_product.sh" \
    --destination "/" \
    --instance-type $instance_type \
    --priority high \
    --name "0_linarg_dot_product" \
    --brief \
    -y

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_benchmark_linarg_dot_product.sh" \
    -iin="/amber/scripts/benchmark_linarg_dot_product.py" \
    -iin="/linear_args/ukb20279/chr21/1_chr21-25863390-46696162/linear_arg.npz" \
    -iin="/linear_args/ukb20279/chr21/1_chr21-25863390-46696162/linear_arg.pvar.gz" \
    -iin="/linear_args/ukb20279/chr21/1_chr21-25863390-46696162/linear_arg.psam.gz" \
    -icmd="bash run_benchmark_linarg_dot_product.sh" \
    --destination "/" \
    --instance-type $instance_type \
    --priority high \
    --name "1_linarg_dot_product" \
    --brief \
    -y