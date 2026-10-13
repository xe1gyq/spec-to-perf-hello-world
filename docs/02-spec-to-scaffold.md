# 02 — From a spec to a scaffold

The dependency chain is:

```text
Need → completed specification → AI instructions → scaffold → implementation → checks → evidence
```

1. Read the blank template and completed matrix specification side by side.
2. Notice that the template asks questions while the specification answers them.
3. Read the three prompts in order. The first plans structure, the second implements, and the third reviews.
4. Inspect the delivered reference files. `src/main.c` implements behavior; the Makefile explains how to build; tests turn acceptance criteria into executable checks.
5. Run `make test`. A successful build alone does not establish correctness.
6. Measure only after correctness checks pass.

To replay generation, use a separate empty directory containing the specification,
template, and prompts. Give an AI the prompts in sequence and inspect each result.
The checked-in reference was prepared with AI assistance; these prompts are reusable
instructions, not a transcript of three separately executed agents.

## Your first change

Propose a new default of 1024 instead of 2048. Update the specification first,
ask the AI to identify affected implementation and documentation, review the diff,
and rerun the checks. The default is a product decision; the generated code follows it.

## Requirement traceability

| Criteria | Evidence |
| --- | --- |
| AC-1 | Quick-start commands and manual validation record |
| AC-2 | `test_checksum`, independent Python sum |
| AC-3 | `test_invalid_arguments` |
| AC-4 | `test_checksum` and `test_help` |
| AC-5 | `make test`, also run by CI |
| AC-6 | Perf lab, profiling script, validation limitations |
