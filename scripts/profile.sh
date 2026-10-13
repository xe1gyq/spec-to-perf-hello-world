#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v perf >/dev/null; then
  echo "perf is missing. See docs/03-perf-lab.md for setup." >&2
  exit 1
fi
mkdir -p results
{
  date -u
  uname -srmo
  gcc --version | head -1
  perf --version
  lscpu
} > results/environment.txt
for mode in row column; do
  perf stat -r 5 -e task-clock,cycles,instructions,cache-references,cache-misses \
    -o "results/${mode}-stat.txt" -- ./build/matrix-scan "$mode" 2048 20 \
    > "results/${mode}-output.txt"
done
perf record -e cpu-clock:u -F 99 -g -o results/column.data -- \
  ./build/matrix-scan column 2048 100
perf report --stdio -i results/column.data > results/column-report.txt
echo "Results saved in results/. Read docs/03-perf-lab.md before interpreting them."
