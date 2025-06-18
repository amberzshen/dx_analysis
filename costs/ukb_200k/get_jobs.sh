# dx find jobs --created-after 2025-02-01 \
#             --created-before 2025-03-13 \
#             --state done \
#             --name get_mat* \
#             -n 100000 \
#             --brief > get_geno_ids.txt

# dx find jobs --created-after 2025-02-01 \
#             --created-before 2025-04-09 \
#             --state done \
#             --name forward_backward* \
#             -n 100000 \
#             --brief > forward_backward_ids.txt

# dx find jobs --created-after 2025-02-01 \
#             --created-before 2025-04-12 \
#             --state done \
#             --name reduction* \
#             -n 100000 \
#             --brief > reduction_ids.txt

# dx find jobs --created-after 2025-02-01 \
#             --created-before 2025-04-09 \
#             --state done \
#             --name linarg_merge* \
#             -n 100000 \
#             --brief > merge_ids.txt

# dx find jobs --created-after 2025-05-02 \
#             --created-before 2025-05-30 \
#             --state done \
#             --name get_mat_chrX* \
#             -n 100000 \
#             --brief > get_geno_chrX_ids.txt

# dx find jobs --created-after 2025-06-04 \
#             --created-before 2025-06-05 \
#             --state done \
#             --name forward_backward\* \
#             -n 100000 \
#             --brief > forward_backward_chrX_ids.txt

# dx find jobs --created-after 2025-06-04 \
#             --created-before 2025-06-05 \
#             --state done \
#             --name reduction\* \
#             -n 100000 \
#             --brief > reduction_chrX_ids.txt

# dx find jobs --created-after 2025-06-10 \
#             --created-before 2025-06-12 \
#             --state done \
#             --name linarg_merge\* \
#             -n 100000 \
#             --brief > merge_chrX_ids.txt

dx find jobs --created-after 2025-05-01 \
            --created-before 2025-06-12 \
            --state done \
            --name add_* \
            -n 100000 \
            --brief > add_ind_ids.txt