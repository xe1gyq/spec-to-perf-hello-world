# 01 — Six hello worlds

## 1. Specification: decide what success means

A specification is a written agreement about behavior. Our first requirement is: “Both traversal modes must return the same correct sum.” A measurable statement is easier to verify than “make it fast.”

## 2. Template: reuse the questions

A template is an empty form: problem, users, inputs, outputs, rules, constraints, and acceptance criteria. Copy it for another feature instead of relying on memory.

## 3. AI-driven: turn decisions into a draft

An AI reads the completed specification and proposes files and code. People decide the requirements and review the result. AI output is a hypothesis until checks provide evidence.

## 4. Scaffolding: provide a starting structure

A scaffold is the initial arrangement of files, build commands, tests, and documentation. Think of a construction frame: it gives work a consistent starting point. This repository includes a working feature so you can see where each part belongs.

## 5. Enterprise software: introduce team habits

Organizations need changes others can understand and verify. This tiny lab introduces bounded inputs, named acceptance criteria, source control, and continuous integration (CI: tests run automatically after a push). Real enterprise systems also need context-specific identity, authorization, deployment, monitoring, and operational ownership.

## 6. Performance: measure the cost of correct work

Latency is how long one task takes. A CPU cache is small, fast storage near the processor. Adjacent data can often be fetched together. Our row mode reads adjacent values; column mode jumps across the array. We hypothesize that rows will be faster for a sufficiently large matrix. Measurement decides whether that happens here.

A profiler helps investigate where execution time goes. A checksum tells us whether the answer is correct. Neither replaces the other.

**Checkpoint:** If column mode returns a different sum but runs faster, is it an optimization? No: it violates the specification.
