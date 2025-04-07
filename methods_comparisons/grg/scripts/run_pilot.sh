
vcf_path="/Users/ambershen/Desktop/linARG/data/pilot_data/chr21-21990355-23324211.vcf.gz"
igd_path="/Users/ambershen/Desktop/linARG/methods_comparisons/grg/grgs/chr21-21990355-23324211.igd"
output_dir="/Users/ambershen/Desktop/linARG/methods_comparisons/grg/grgs/chr21-21990355-23324211.grg"

grg convert $vcf_path $igd_path
grg construct $igd_path -o $output_dir