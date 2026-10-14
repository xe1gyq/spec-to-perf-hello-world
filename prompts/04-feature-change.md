# Prompt 4 — Evolve an existing feature from a specification

Use this reusable interaction sequence with the relevant feature number.

1. **Define:** Read the existing specifications and template. Propose a small additive feature, its interface, non-goals, and measurable acceptance criteria. Write `specs/<next-number>-<feature>.md` before implementation. Explain how it extends prior specs and make assumptions visible.
2. **Challenge:** Identify boundary cases and distinguish correctness requirements from performance hypotheses. Map acceptance criteria to independent checks. Resolve routine choices explicitly; ask the owner if a decision changes the requested scope.
3. **Test:** Add tests for the new contract. Run them against the existing binary and record the expected failure. Confirm the failure concerns missing behavior, not a broken test setup.
4. **Implement:** Make the smallest change that satisfies the specification while preserving previous contracts. Run the full tests and inspect the diff for unintended behavior.
5. **Measure:** Run a documented controlled workload only after correctness passes. Preserve raw results and environment metadata; distinguish observation from causal explanation. Report unavailable tools honestly.
6. **Review and teach:** Map each criterion to evidence, record limitations and unresolved items, and write a beginner walkthrough of the decisions. Label illustrative prompts as examples, not verbatim transcripts.
7. **Deliver:** Package specification, code, checks, evidence, and explanation in one reviewable commit when requested. A single commit is a delivery boundary, not evidence of the order in which work happened.

Do not rewrite historical measurements. Keep repository content in English.
