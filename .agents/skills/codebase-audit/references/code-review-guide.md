# Code review guide

Use this guide during Phase 2 of `codebase-audit`.

Review the codebase as a whole, not just isolated snippets.

## Scope

Focus on the most important engineering risks and tradeoffs:

- Architecture and separation of responsibilities
- Security weaknesses and risky data handling
- Code quality and maintainability
- Bugs, edge cases, and reliability issues
- Technical debt and outdated patterns
- Positive implementation choices worth keeping

## How to review

1. Explore the repository before drawing conclusions.
2. Prioritize high-impact findings over stylistic comments.
3. Look for concrete evidence in the code, not generic advice.
4. Prefer findings that affect production safety, correctness, maintainability, or handover risk.
5. Mention positive observations when they are meaningful.

## What to check

### Architecture

- Is the architecture intentional and reasonably consistent?
- Are responsibilities clearly separated?
- Are there god modules, hidden coupling, or brittle dependencies?
- Are important flows easy to trace?

### Security

- Hard-coded secrets or credentials
- Input validation gaps
- Authentication or authorization weaknesses
- Unsafe data access patterns
- XSS, CSRF, injection, deserialization, or path traversal risks
- Dependency risks that are obvious from the manifests or code

### Code quality

- Unclear naming or inconsistent conventions
- Missing or weak error handling
- Dead code, stale TODOs, commented-out code
- Excessive duplication
- Hard-coded values that should be configuration or constants
- Missing tests around critical behavior

### Reliability

- Logic errors or fragile assumptions
- Race conditions or ordering problems
- Null or undefined handling issues
- Time, timezone, or encoding pitfalls
- Incomplete edge-case handling

### Technical debt

- Deprecated libraries or patterns
- Legacy workarounds that increase risk
- Areas that are difficult to change safely
- Missing documentation for non-obvious behavior

## Output format

Write the result using this structure:

```markdown
## Audit Report

1. Summary
[3-5 sentences on overall health]

2. Critical findings
- [must fix before production or handover]

3. Significant findings
- [should fix soon]

4. Minor findings
- [nice to have]

5. Positive observations
- [clear strengths worth keeping]
```

Rate overall health as:

- `Good`
- `Needs Improvement`
- `Requires Significant Work`

## Review rules

- Be specific about why an issue matters.
- Reference concrete files or modules when possible.
- Do not flood the report with low-value style notes.
- Group similar findings together.
- If no major problems are found, say so clearly.
- Keep the audit useful for a client inheriting or evaluating the codebase.
