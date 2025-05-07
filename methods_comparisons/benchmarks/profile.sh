#!/bin/bash

### Example usage ###
# bash profile.sh my_output.csv python3 -c "sum([i**2 for i in range(1000000)])"

apt update && apt install -y time

# Check input
if [ $# -lt 2 ]; then
  echo "Usage: $0 output.csv command [args...]"
  exit 1
fi

# Get output file and shift to access the command
OUTPUT_FILE="$1"
shift
COMMAND=("$@")

# Number of runs (change if needed)
RUNS=10

# Write CSV header
echo "run,wall_time_seconds,peak_memory_MB" > "$OUTPUT_FILE"

# Run the command repeatedly
for i in $(seq 1 $RUNS); do
  echo "Running iteration $i..."

  /usr/bin/time -v "${COMMAND[@]}" 2>&1 | awk -v run="$i" -v out="$OUTPUT_FILE" '
    /Elapsed \(wall clock\) time/ {
      split($NF, t, ":")
      if (length(t) == 2) {
        wall = t[1] * 60 + t[2]
      } else if (length(t) == 3) {
        wall = t[1] * 3600 + t[2] * 60 + t[3]
      }
    }
    /Maximum resident set size/ {
      mem = $NF / 1024
    }
    END {
      printf "%d,%.3f,%.2f\n", run, wall, mem >> out
    }'
done

echo "Results saved to $OUTPUT_FILE"