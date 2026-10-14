# Spec to Perf: Hello World

A beginner-friendly, English-language lab for **AI-driven specification templates and software scaffolding**, using a tiny C binary and Linux `perf`.

**Question:** Can two programs do the same work correctly but take different amounts of time?

We store a square matrix (a grid of numbers) in one continuous array. The modes read it row by row, column by column, or in 32 × 32 tiles. All must produce the same checksum (the sum of all values across all repetitions).

## Start here

1. Read [the concepts](docs/01-concepts.md): no programming background required.
2. Compare the [blank template](templates/feature-spec.md) with the [completed specification](specs/001-matrix-scan.md).
3. Follow [the AI and scaffolding exercise](docs/02-spec-to-scaffold.md).
4. Build the binary, then follow [the perf lab](docs/03-perf-lab.md).
5. Read [the original validation record](docs/04-validation.md).
6. Follow [feature 002, interaction by interaction](docs/05-feature-002-walkthrough.md): a complete additive change in one commit, with [new measurements](docs/06-blocked-validation.md).

## Run your first binary

Requirements: Linux, GCC, Make, and Python 3. `perf` is needed only for profiling.

```sh
make
./build/matrix-scan --help
./build/matrix-scan row 4 1
./build/matrix-scan column 4 1
make test
make demo
```

For the 4 × 4 example, both modes print `checksum=120`. Elapsed time varies.
`make` compiles human-readable C into `build/matrix-scan`, an executable binary.
`make test` checks correctness. `make demo` runs a larger experiment.

```sh
make profile
```

This records performance evidence under `results/` when `perf` and the required kernel permissions are available. Read the lab if counters are unavailable.

## What is in the scaffold?

| Path | Purpose |
| --- | --- |
| `templates/` | Reusable questions for future features |
| `specs/` | Decisions and acceptance criteria for this feature |
| `prompts/` | Instructions an AI can follow |
| `src/` | The implementation |
| `tests/` | Executable correctness checks |
| `scripts/` | Repeatable measurement commands |
| `.github/workflows/` | Automated build and tests on GitHub |
| `docs/` | Lessons and evidence |

This repository is a completed reference scaffold generated with AI assistance and checked locally. It introduces enterprise habits—traceable requirements, input bounds, reproducible builds, review, and automated checks—through one local tool. It is not a production enterprise application.

## Feature 002: blocked traversal

```sh
./build/matrix-scan blocked 33 1
bash scripts/profile-002.sh
```

Read [specification 002](specs/002-blocked-scan.md) before the implementation. The dedicated script compares all three modes; `make profile` retains the original two-mode lesson.
