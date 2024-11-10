#!/bin/bash
# mtx_path="/mnt/project/linear_arg_results/10mb-200kb-window-test_chr1-150000001-160000000/genotype_matrices/27_chr1-155400001-155600000.npz"
# variant_path="/mnt/project/linear_arg_results/10mb-200kb-window-test_chr1-150000001-160000000/variant_metadata/27_chr1-155400001-155600000.txt"
# out="debug_counts/27_chr1-155400001-155600000/"

# mtx_path="/mnt/project/linear_arg_results/10mb-200kb-window-test_chr1-150000001-160000000/genotype_matrices/0_chr1-150000001-150200000.npz"
# variant_path="/mnt/project/linear_arg_results/10mb-200kb-window-test_chr1-150000001-160000000/variant_metadata/0_chr1-150000001-150200000.txt"
# out="debug_counts/0_chr1-150000001-150200000/"

# mtx_path="/mnt/project/linear_arg_results/1mb-100kb-debug-counts_chr1-12500001-13500000/genotype_matrices/7_chr1-13200001-13300000.npz"
# variant_path="/mnt/project/linear_arg_results/1mb-100kb-debug-counts_chr1-12500001-13500000/variant_metadata/7_chr1-13200001-13300000.txt"
# out="debug_counts/7_chr1-13200001-13300000/"
# instance_type="mem3_ssd1_v2_x4"

# mtx_path="/mnt/project/linear_arg_results/500kb-50kb-debug-counts_chr1-12500001-13000000/genotype_matrices/7_chr1-12850001-12900000.npz"
# variant_path="/mnt/project/linear_arg_results/500kb-50kb-debug-counts_chr1-12500001-13000000/variant_metadata/7_chr1-12850001-12900000.txt"
# out="debug_counts/7_chr1-12850001-12900000/"
# instance_type="mem3_ssd1_v2_x4"

# mtx_path="/mnt/project/linear_arg_results/50kb-5kb-debug-counts_chr1-12000001-12050000/genotype_matrices/9_chr1-12045001-12050000.npz"
# variant_path="/mnt/project/linear_arg_results/50kb-5kb-debug-counts_chr1-12000001-12050000/variant_metadata/9_chr1-12045001-12050000.txt"
# out="debug_counts/9_chr1-12045001-12050000/"
# instance_type="mem1_ssd1_v2_x4"

# dx run app-swiss-army-knife \
#     -iin="/amber/scripts/run_debug_counts.sh" \
#     -iin="amber/scripts/debug_counts.py" \
#     -icmd="bash run_debug_counts.sh $mtx_path $variant_path $out" \
#     --destination "/" \
#     --instance-type $instance_type \
#     --priority low \
#     --name "debug_counts" \
#    --brief \
#     -y

# res_dirs=("debug_counts/27_chr1-155400001-155600000/" "debug_counts/0_chr1-150000001-150200000/")


instance_type="mem1_ssd1_v2_x2"
load_dir="/mnt/project/"
res_dir="debug_counts/9_chr1-12045001-12050000/"
graph_types=("brick_graph" "recom" "linarg")

for start in `seq 0 25000 399999`; do 
	end=$(( start+25000 )) 
    echo $start $end

    for graph_type in "${graph_types[@]}"; do

        dx run app-swiss-army-knife \
            -iin="/amber/scripts/run_debug_counts.sh" \
            -iin="amber/scripts/debug_counts.py" \
            -icmd="bash run_debug_counts.sh $res_dir $load_dir $graph_type $start $end" \
            --destination "/" \
            --instance-type $instance_type \
            --priority low \
            --name "get_geno_${res_dir}_${graph_type}_${start}_${end}" \
            --brief \
            -y
    done
done
