instance_type="mem3_ssd1_v2_x32" # 256GB

dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_benchmark_matmat.sh" \
    -iin="/amber/scripts/benchmark_matmat.py" \
    -icmd="bash run_benchmark_matmat.sh" \
    --destination "/amber/" \
    --instance-type $instance_type \
    --priority high \
    --name "benchmark_matmat" \
    --brief \
    -y