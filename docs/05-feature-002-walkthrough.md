# 05 — One feature, one commit, the complete learning loop

This lesson follows the actual addition of blocked traversal. Start with [specification 002](../specs/002-blocked-scan.md), then review tests, code, and [evidence](06-blocked-validation.md). All these artifacts are delivered together in one commit.

## Why a file named 002?

`001` describes the original contract; `002` describes an additive change. The number is our project's ordering convention, not an industry standard or an executable instruction. The AI does not infer your intended process from numbering alone: its prompt must tell it to read and honor the specification.

We used the same sections as [the feature template](../templates/feature-spec.md). We kept 001 as the baseline and made precedence explicit in 002: the new mode extends the old list of modes, while existing behavior remains valid. A future incompatible change must state what it replaces and how users migrate.

## Interaction 1 — Turn a request into a contract

**Owner intent:** add a small feature and make the specification-driven workflow visible in one commit.

**AI proposal:** add blocked matrix traversal. Fix the tile size at 32 so the learning exercise stays bounded.

**Decision:** preserve the CLI shape and output fields; add only the mode. Process columns inside each tile so the experiment retains column traversal locally. Do not add an adjustable tile parameter yet.

**Artifact:** `specs/002-blocked-scan.md` was written before implementation.

**Lesson:** the specification contains decisions that code would otherwise silently invent. The owner delegated this small feature choice; no separate approval conversation is being claimed.

## Interaction 2 — Separate requirements from hypotheses

**Requirement:** every value must contribute once, including cells in incomplete tiles.

**Hypothesis:** blocked traversal may outperform full column traversal.

**Decision:** test dimensions 31, 32, and 33 around the boundary, plus multiple tiles and maximum size. Preserve independent checksum calculation. Do not require a speedup in CI.

**Lesson:** “correct” can be a hard acceptance condition; “faster” needs a defined experiment and evidence. A result that disproves the speed hypothesis can still be a successful learning feature.

## Interaction 3 — Make missing behavior visible

The new tests ran against the existing binary. The suite failed 15 assertions because `blocked` and its help entry did not exist. The before log is saved with the evidence.

**Lesson:** an expected failing test connects the requirement to a real absence in the program. This test-first technique is useful here, but specification-driven development does not require every project to use this exact sequence.

## Interaction 4 — Implement the smallest change

The implementation adds a named block-size constant and `sum_blocked`, extends mode validation/help, and selects the new function. Existing initialization, validation, checksum checking, and timing are reused.

Imagine a 33 × 33 matrix: along either dimension it has one full span of 32 and one final span of 1. Each tile end is clipped to the matrix edge. This is why testing only 32 × 32 would have missed an important class of bugs.

**Lesson:** the code implements the contract; its simplicity comes from deciding scope first. The scaffold already exists, so evolving it does not mean regenerating the project.

## Interaction 5 — Verify correctness, then measure

The complete six-method test suite passed. A dedicated script measured all three modes and collected a blocked profile. The implementation was not altered to chase a favorable benchmark.

**Observation:** blocked took about 0.066 s versus column's 0.479 s and row's 0.044 s on this host. Blocked improved on columns but did not beat rows.

**Lesson:** evidence can support a narrower claim than the one we initially hoped for. Keep that distinction visible.

## Interaction 6 — Review against the contract

The validation document maps AC-1 through AC-5 to tests, source review, or measurements. Raw text is saved alongside the explanation. Review the contract and evidence before accepting the feature; an AI summary alone is not proof.

**Lesson:** every acceptance criterion needs an appropriate check. Tests establish selected behaviors, source inspection checks structure, and perf provides observations. They answer different questions.

## Interaction 7 — Package one reviewable delivery

The commit contains:

| Artifact | Reviewer question |
| --- | --- |
| `specs/002-blocked-scan.md` | What change was intended? |
| `prompts/04-feature-change.md` | How can I repeat the interaction sequence? |
| `tests/test_cli.py` | Which behaviors are checked? |
| `src/main.c` | How was the contract implemented? |
| `scripts/profile-002.sh` | How can I reproduce the experiment? |
| `docs/evidence/002/` | What actually happened? |
| This lesson and validation report | What should I learn, and what remains uncertain? |

One commit is the requested delivery unit. Git stores the final snapshot, not the chronology of edits inside it. The work order above is a documented account supported by captured logs, not a claim that Git proves the sequence. The reusable prompt file is a teaching aid, not a verbatim transcript of separate user messages or agents.

## Try the feature

```sh
make test
./build/matrix-scan blocked 33 1
bash scripts/profile-002.sh
```

Before running the 33 × 33 example, predict whether the final partial tiles are visited. Then compare the checksum with row mode. For the next interaction, propose one behavior change in words before editing code. Use the template to turn it into a contract, and ask what evidence would convince you it works.
