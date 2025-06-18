# dx find jobs --created-after 2025-04-11 \
#             --created-before 2025-06-16 \
#             --state done \
#             --name get_mat* \
#             -n 100000 \
#             --brief > get_geno_ids.txt
# need to subtract off chrX from no filt

# dx find jobs --created-after 2025-05-26 \
#             --created-before 2025-06-16 \
#             --state done \
#             --name forward_backward* \
#             -n 100000 \
#             --brief > forward_backward_ids.txt

# dx find jobs --created-after 2025-05-30 \
#             --created-before 2025-06-12 \
#             --state done \
#             --name reduction* \
#             -n 100000 \
#             --brief > reduction_ids.txt

# dx find jobs --created-after 2025-06-01 \
#             --created-before 2025-06-11 \
#             --state done \
#             --name linarg_merge* \
#             -n 100000 \
#             --brief > merge_ids.txt

dx find jobs --created-after 2025-06-10 \
            --created-before 2025-06-17 \
            --state done \
            --name add_* \
            -n 100000 \
            --brief > add_ind_ids.txt
