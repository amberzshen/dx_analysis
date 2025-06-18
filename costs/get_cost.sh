cat 2505_jobs.txt | xargs -P64 -I{} bash -c "dx describe {} | grep Price" | tr -d '£' > 2505_costs.txt
cat 2505_costs.txt | tr -d '£' | awk '{sum+=$3; print sum}'