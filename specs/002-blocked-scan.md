# 002 — Blocked matrix traversal

Status: implemented and locally validated; see the linked evidence.

## Problem and user
A learner wants to evolve the existing program through a specification-driven change and investigate whether processing small tiles improves on column traversal.

## Scope and non-goals
Add one `blocked` mode using fixed 32 × 32 tiles. No adjustable tile argument, threading, new dependencies, or guaranteed speedup. Preserve the row and column interfaces from specification 001. This document extends 001; where its list of supported modes differs, 002 adds `blocked`. All other limits and error contracts remain in force.

## Interface and data
`matrix-scan blocked [size] [repeats]`

Use the existing defaults (2048 and 20), limits (1..4096 and 1..1000), initialization, output keys, checksum verification, and exit statuses. Iterate tile rows, tile columns, columns inside each tile, then rows inside each tile. Clip the final tiles to the matrix boundaries. The block size is a named constant of 32 elements per side.

## Functional requirements
- FR-1: Read every matrix element exactly once per repetition, including partial tiles.
- FR-2: Reuse existing allocation, timing, checksum, and validation behavior.
- FR-3: Expose a non-inlined `sum_blocked` symbol and retain volatile reads.
- FR-4: Preserve existing row and column behavior and output fields.

## Performance hypothesis
Limiting column traversal to small tiles may reduce cache misses and elapsed time versus full-height column traversal. Row traversal remains a comparison baseline and may still be faster. A 32 × 32 tile contains 4 KiB of values but those values are not a contiguous 4 KiB memory region. Tile size is an educational choice, not an empirically tuned optimum.

## Acceptance criteria
- AC-1: `blocked 4 1` returns checksum 120; blocked mode matches an independent oracle for sizes 1, 31, 32, 33, 65 and repeats 1 and 3.
- AC-2: The maximum dimension (4096, one repetition) returns the correct checksum; omitted arguments retain the specified defaults.
- AC-3: Invalid sizes/repetitions and extra arguments in blocked mode exit 2, including zero, negative, malformed, overflow, and above-limit values. Help lists all three modes.
- AC-4: All existing tests pass, and source inspection confirms clipped loops, one visit per element, a named symbol, and volatile reads.
- AC-5: Collect a reproducible three-mode experiment, preserve raw text and environment metadata, and explain results without requiring a speedup to pass.

## Measurement plan
Use one optimized binary, size 2048, 20 repetitions and five perf stat runs per mode, with user-space cycles, instructions, and cache events. Capture actual commands, compiler and source hashes. Record a separate 100-repetition blocked profile. Whole-process perf times include setup. Keep historical 001 evidence intact. Sequential mode order is a limitation; shared-host noise and CPU-specific cache events limit generalization.

## Scaffold and review
Extend `src/main.c`, `tests/test_cli.py`, and `README.md`. Add a dedicated profiling script, a reusable change prompt, this spec, a learning walkthrough, and a validation report. Leave the original two-mode profiling script usable. Review partial-tile bounds and old-mode compatibility before accepting performance claims.

## Operational constraints
No new allocation or privileged operation in the binary. Use existing host profiling permissions. CI asserts correctness, never a timing ratio. One commit packages the full change; the walkthrough records work order because a single Git commit cannot prove the temporal order of editing.
