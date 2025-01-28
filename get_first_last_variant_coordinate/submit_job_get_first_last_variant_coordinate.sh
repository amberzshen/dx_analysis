#!/bin/bash

dx run app-swiss-army-knife \
    -iin="/amber/scripts/get_first_last_variant_coordinate.sh" \
    -icmd="bash get_first_last_variant_coordinate.sh" \
    --destination "/GRCh38_metadata" \
    --instance-type "mem1_ssd1_v2_x4" \
    --priority low \
    --name get_first_last_variant_coordinate \
    -y
