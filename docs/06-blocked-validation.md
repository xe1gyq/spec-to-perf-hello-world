# 06 — Feature 002: acceptance and measurement

Recorded 2026-10-14 on the same development machine. Exact environment, source/build hashes, flags, raw counters, and program output are in [the evidence directory](evidence/002). Reproduce with `make test` and `bash scripts/profile-002.sh`. Historical feature 001 evidence is unchanged.

## Acceptance review

| Criterion | Check and outcome |
| --- | --- |
| AC-1 | `test_blocked_edges`: independent arithmetic oracle for dimensions 1, 4, 31, 32, 33, 65; repeats 1 and 3. PASS. |
| AC-2 | `test_blocked_edges` includes 4096 with one repetition; `test_blocked_defaults` checks omitted size/repetitions and checksums. PASS. |
| AC-3 | `test_blocked_invalid_arguments` and `test_help`. PASS. |
| AC-4 | Full six-method suite passes; previous row/column tests retained. Source review: disjoint tiles cover [0,n) in each dimension, clipped end bounds prevent overrun, nested inner loops visit each cell once, `sum_blocked` is non-inlined and reads volatile data. PASS. |
| AC-5 | Five perf stat processes per mode and a separate sampled profile completed. Commands and raw output saved. PASS. |

Before implementation, the expanded suite reported 15 failures because valid blocked invocations and help were unsupported. After implementation, all six test methods passed. These are actual execution logs: [before](evidence/002/before-implementation.txt), [after](evidence/002/after-implementation.txt). Passing rejection tests against the old binary alone would not demonstrate support for the new mode.

## Measured results

One optimized binary, size 2048, 20 traversals, five processes per mode. Mean whole-process elapsed time from perf stat:

| Metric | Row | Column | Blocked |
| --- | ---: | ---: | ---: |
| Elapsed seconds | 0.043652 | 0.479470 | 0.066335 |
| User-space cycles | 164,598,044 | 1,937,404,440 | 258,998,411 |
| User-space instructions | 478,597,833 | 646,534,237 | 586,957,952 |
| User-space cache misses | 5,317,046 | 75,839,052 | 4,567,399 |

All 15 runs returned checksum 10485612420. Blocked was about 7.23× faster than column in elapsed time, while row was about 1.52× faster than blocked. Therefore this feature improves on column mode in this experiment but is not the fastest way to sum this matrix.

Blocked also registered fewer generic cache misses than row despite taking longer. This is a useful lesson: one counter is not the objective. Instructions, access patterns, and other CPU behavior matter too. The evidence is consistent with the locality hypothesis, not a complete causal decomposition.

The separate 100-traversal blocked profile collected 30 cpu-clock samples, zero lost, all attributed to `sum_blocked` self time. That locates the observed hotspot but is a small sample; do not use it to claim precise instruction costs.

## Limits and next experiment

Modes ran sequentially row → column → blocked on a shared, unpinned host. Whole-process time includes initialization; internal timer output measures traversal only. Generic cache events are CPU-specific. No guaranteed ratio or universal best tile size follows from these observations. The script writes environment data and text evidence; binary recordings remain ignored locally.

A future spec could expose tile size and compare several sizes under an interleaved experiment. That change would need its own input contract and boundary checks before performance testing.
