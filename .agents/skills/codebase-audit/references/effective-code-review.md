# Effective code review (full codebase)

Use this when auditing an inherited or unfamiliar codebase—not only a pull request diff.

**Repository size:** always align depth and claims with **`large-repository-strategy.md`** (after running **`scripts/repo_scope_hint.py`** or equivalent). On medium/large tiers, “review the codebase” means **risk-weighted sampling**, not every file line-by-line.

## Mindset

- **Seek understanding first.** Map entry points, data flow, and ownership boundaries before judging style.
- **Be proportional.** A prototype and a payment service do not share the same bar for security or rigor.
- **Separate facts from opinions.** Label uncertainty (“possible race”, “needs verification”) instead of stating guesses as facts.

## How to explore efficiently

1. **Start from the edges.** CLIs, HTTP handlers, workers, and `main`/`index` files show what the system actually does.
2. **Follow one vertical slice.** Pick one user-visible feature and trace it UI/API → service → persistence → external calls.
3. **Read dependency manifests.** Lockfiles and `package.json` / `pyproject.toml` / `go.mod` reveal frameworks, risky packages, and version drift.
4. **Skim tests and CI.** They document intended behavior and show what the team already protects.
5. **Note “hot” files.** Files with high churn or huge line counts often concentrate risk; prioritize them after the slice above.

## What to look for (checklist)

### Architecture and structure

- Clear layering or boundaries (or absence of them): who may call whom?
- Modules that do too much (“god” objects) or leak internals across layers.
- Consistency: do similar problems get similar solutions, or is every folder a new pattern?
- Fit for scale: obvious bottlenecks, synchronous calls that should be async, missing pagination, N+1 queries.

### Security

- Secrets, tokens, or private keys in source or logs.
- AuthZ vs authN: are permissions enforced on the server for every sensitive action?
- Input validation and output encoding (injection, XSS, path traversal, SSRF).
- Dependency and supply-chain risk: abandoned packages, known CVEs, unpinned versions in prod paths.

### Reliability and operations

- Error handling: failures surfaced, retried, or swallowed?
- Observability: structured logs, metrics, tracing where failures are costly.
- Configuration: safe defaults, documented env vars, feature flags if relevant.

### Maintainability

- Naming, module boundaries, duplication that will diverge.
- Dead code, commented-out blocks, stale TODOs without owners.
- Test quality vs coverage: flaky tests, missing integration tests for critical paths.

## How to write findings

- **One issue per bullet** with **impact** (what breaks or degrades) and **location** (path, symbol, or area).
- **Severity:** align with the audit skill—Critical / Significant / Minor—and justify Critical items in one line.
- **Balance:** include genuine strengths (patterns, tests, docs) so the report is credible.

## When the codebase is huge

- **Sample deliberately:** representative modules plus security-sensitive and high-churn areas.
- **State the scope** in the audit summary (what you reviewed deeply vs spot-checked).
