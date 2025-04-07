git clone https://github.com/quattro/linear-dag.git
curl -fsSL https://install.julialang.org | sh
. /home/dnanexus/.bashrc

julia linear-dag/julia/InstallDependencies.jl
julia linear-dag/julia/benchmark_script.jl  "/mnt/project/1kg/1kg_chr1_julia"