# 04 — Actual validation record

Recorded on 2026-10-13. CPU: Intel Core i7-8809G; Linux 6.12.0-264.el10.x86_64; CentOS Stream 10; GCC 14.4.1. Build flags are in the Makefile.

## Correctness

- `make test`: PASS (three test methods with parameterized checksum and invalid-input cases).
- Both modes with size 4, repeats 1: checksum 120.
- Compilation: `-O2 -g -std=c11 -Wall -Wextra -Werror -fno-omit-frame-pointer`.

## Internal traversal timing

Five runs per mode, alternating which mode ran first each round; size 2048, repeats 20. The host was not isolated or CPU-pinned. These are observations, not a benchmark guarantee.

```text
mode=row size=2048 repeats=20 checksum=10485612420 elapsed_seconds=0.038625
mode=column size=2048 repeats=20 checksum=10485612420 elapsed_seconds=0.522484
mode=column size=2048 repeats=20 checksum=10485612420 elapsed_seconds=0.521250
mode=row size=2048 repeats=20 checksum=10485612420 elapsed_seconds=0.039287
mode=row size=2048 repeats=20 checksum=10485612420 elapsed_seconds=0.038782
mode=column size=2048 repeats=20 checksum=10485612420 elapsed_seconds=0.519474
mode=column size=2048 repeats=20 checksum=10485612420 elapsed_seconds=0.518289
mode=row size=2048 repeats=20 checksum=10485612420 elapsed_seconds=0.038875
mode=row size=2048 repeats=20 checksum=10485612420 elapsed_seconds=0.039120
mode=column size=2048 repeats=20 checksum=10485612420 elapsed_seconds=0.523482
```

Median row time: 0.038875 s. Median column time: 0.521250 s. Observed column/row ratio: 13.41.

Both modes produced the same checksum. The observed timing supports further investigation of traversal order. It does not establish a measured cache-miss cause.

## Perf status

`perf` was not installed. An attempted `sudo -n dnf install -y perf` required an administrator password. No perf counters or sampled profiles were collected in this validation. Run `make profile` after installation on a permitted host. Hardware-counter and hotspot conclusions remain pending.

## Acceptance status

AC-1 through AC-5 passed locally. AC-6 is satisfied by documented commands and an explicit unavailable-tool record. A successful local test does not imply the GitHub CI run has completed.
