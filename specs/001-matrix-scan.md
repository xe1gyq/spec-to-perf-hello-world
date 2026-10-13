# 001 — Matrix scan

## Problem and user
A beginner wants to connect a written requirement to generated code and measured performance.

## Scope and non-goals
Build one Linux C CLI with two traversal orders. No service, network, database, concurrency, or production performance guarantee.

## Interface and data
`matrix-scan {row|column} [size] [repeats]`
Defaults: size 2048, repeats 20. Decimal integers only, size 1..4096, repeats 1..1000. Allocate size² unsigned 32-bit values; value at linear index i is i modulo 251. Sum into an unsigned 64-bit integer. Memory for the matrix is at most 64 MiB. Maximum total sum fits in 64 bits.

Output: mode, size, repeats, checksum, elapsed_seconds. Time only repeated traversal with a monotonic clock. Invalid arguments: stderr and exit 2. Allocation, clock, or checksum failure: exit 1. Success and `--help`: exit 0.

## Functional requirements
- FR-1: Row and column modes visit every value once per repetition.
- FR-2: Check the accumulated sum against a reference produced during initialization.
- FR-3: Reject malformed and out-of-range input before allocation.
- FR-4: Preserve repeated reads under optimization and expose named scan functions to a profiler.

## Performance hypothesis
Rows should benefit from spatial locality on sufficiently large matrices. The effect depends on caches, hardware, dimensions, compiler, and system load. Volatile reads intentionally constrain optimization for this teaching experiment; results do not describe all matrix software.

## Acceptance criteria
- AC-1: Both modes with size 4 and one repeat produce checksum 120.
- AC-2: Both modes match an independent mathematical oracle for several dimensions and repetitions.
- AC-3: Missing mode, unknown mode, zero, negatives, text, overflow, excess arguments, and values above limits exit 2.
- AC-4: Valid runs print nonnegative traversal time; `--help` exits 0.
- AC-5: `make test` passes with warnings treated as errors.
- AC-6: Profiling commands and environment capture are documented. If perf cannot run, report that fact instead of inventing counters.

## Measurement plan
Use the same optimized binary, dimensions, and repetitions for both modes. Repeat each perf stat command five times. Record environment and raw output. Compare elapsed time, cycles, instructions, and supported cache events. Profile column mode to locate its hot function. Separate whole-process perf measurement from internal traversal timing.

## Scaffold and review
Generate the tree described in README. Review indexing, numeric limits, checksums, compiler observability, errors, and claims before accepting output.

## Operational constraints
Local synthetic data only. No privileged execution required for correctness. Profiling may require administrator-approved host settings. CI checks correctness and does not assert a timing ratio on shared runners.
