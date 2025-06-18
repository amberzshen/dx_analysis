dx upload phenotype_fieldnames_20250617.txt --path='/phenotypes/'

dx run table-exporter \
    -idataset_or_cohort_or_dashboard=/app86805_20241111195915.dataset \
    -ientity="participant" \
    -ioutput="phenotypes_raw_20250617" \
    -ioutput_format="CSV" \
    -icoding_option="RAW" \
    -iheader_style="FIELD-NAME" \
    -ifield_names_file_txt="/phenotypes/phenotype_fieldnames_20250617.txt" \
    --destination=/phenotypes/ -y