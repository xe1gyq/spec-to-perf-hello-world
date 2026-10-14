#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v perf >/dev/null || { echo 'perf is required' >&2; exit 1; }
make all
out=results/002
mkdir -p "$out"
{
  date -u
  uname -srmo
  gcc --version | head -1
  perf --version
  lscpu | sed -n '1,28p'
  sha256sum src/main.c Makefile build/matrix-scan
} > "$out/environment.txt"
for mode in row column blocked; do
  perf stat -r 5 -e cycles:u,instructions:u,cache-references:u,cache-misses:u \
    -o "$out/$mode-stat.txt" -- ./build/matrix-scan "$mode" 2048 20 \
    > "$out/$mode-output.txt"
done
perf record -e cpu-clock:u -F 99 -g -o "$out/blocked.data" -- \
  ./build/matrix-scan blocked 2048 100 > "$out/blocked-record-output.txt"
perf report --stdio -i "$out/blocked.data" > "$out/blocked-report.txt"
echo "Evidence written to $out"
