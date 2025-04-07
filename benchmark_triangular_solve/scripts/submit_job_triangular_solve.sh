instance_type="mem3_ssd1_v2_x4" # 32GB
dx run app-swiss-army-knife \
    -iin="/amber/scripts/run_triangular_solve.sh" \
    -iin="/amber/scripts/triangular_solve.py" \
    -icmd="bash run_triangular_solve.sh" \
    --destination "/" \
    --instance-type $instance_type \
    --priority high \
    --name "1kg_triangular_solve_benchmark" \
    --brief \
    -y
