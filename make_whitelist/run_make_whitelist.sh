#!/bin/bash

set -euo pipefail

pip install polars
pip install numpy
python3 make_whitelist.py