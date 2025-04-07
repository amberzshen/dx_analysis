git clone https://github.com/quattro/linear-dag.git
curl -fsSL https://install.julialang.org | sh -s -- -y
. /home/dnanexus/.bashrc

julia linear-dag/julia/InstallDependencies.jl 
julia linear-dag/julia/benchmark_script.jl  "/mnt/project/methods_comparisons/linarg/0_chr21-5030618-25863389_julia"
julia linear-dag/julia/benchmark_script.jl  "/mnt/project/methods_comparisons/linarg/1_chr21-25863390-46696162_julia"