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

## Completed perf analysis

After installing perf 6.12.0-275.el10.x86_64, `make profile` completed successfully on the same host. The kernel's `perf_event_paranoid` value was 2; no policy changes were made. The binary was built from commit `1cd3b35` with the Makefile flags above. This measurement ran five row processes followed by five column processes, with size 2048 and 20 traversals each. The host was not isolated or CPU-pinned.

| Measurement (perf stat, five runs) | Row | Column | Column / row |
| --- | ---: | ---: | ---: |
| Whole-process elapsed seconds | 0.047009 | 0.539550 | 11.48× |
| User-space task-clock, milliseconds | 46.49 | 538.29 | 11.58× |
| User-space cycles | 165,865,897 | 2,000,410,714 | 12.06× |
| User-space instructions | 478,599,981 | 646,536,439 | 1.35× |
| User-space cache references | 11,450,622 | 90,228,849 | 7.88× |
| User-space cache misses | 7,429,117 | 78,328,704 | 10.54× |

All ten runs produced checksum `10485612420`. These whole-process times include setup and differ from the earlier traversal-only timer results. Counter scope is user space, as indicated by `:u` in the raw output.

### Beginner interpretation

Both approaches give the correct answer. Columns require substantially more cycles and register substantially more cache misses on this machine. This is consistent with worse memory locality: row mode reads adjacent four-byte values, whereas column mode jumps 8,192 bytes between reads at dimension 2048. The matrix occupies 16 MiB, larger than this CPU's reported 8 MiB L3 cache.

This experiment supports the locality hypothesis; it does not isolate every cause. Instruction counts also differ, and stride, translation, prefetching, cache behavior, and system load can contribute. Generic cache events are CPU-dependent and must not be described as specifically L1 misses.

### Hotspot analysis

`perf record -e cpu-clock:u -F 99 -g` sampled column mode with 100 traversals. It collected 259 samples, with zero lost samples. `perf report` attributed 100% of the observed self samples to `sum_columns`. This identifies the main loop as the observed hotspot; finite sampling does not mean setup literally takes no time.

`perf annotate --stdio -i results/column.data --symbol sum_columns` placed 96.14% of local sample weight at the pointer increment immediately after the array load. Sample placement does not establish that the increment itself causes the delay. CPU-clock samples are not precise instruction-latency measurements.

### Saved evidence

The following small text artifacts are committed so readers can inspect actual output without needing the original binary profile:

- [Row counters](evidence/2026-10-13/row-stat.txt)
- [Column counters](evidence/2026-10-13/column-stat.txt)
- [Row program output](evidence/2026-10-13/row-output.txt)
- [Column program output](evidence/2026-10-13/column-output.txt)
- [Sampled hotspot report](evidence/2026-10-13/column-report.txt)

The binary recording remains locally in `results/column.data`. Re-run `make profile` to generate your own recording and environment details.

## Acceptance status

AC-1 through AC-5 passed locally. The initial GitHub build and acceptance-test workflow also passed. AC-6 now has actual perf counters and sampled hotspot evidence, in addition to the documented commands. No application code changed during this profiling follow-up.
