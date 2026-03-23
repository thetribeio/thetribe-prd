# Large repository strategy (audit scope)

Use this after **`scripts/repo_scope_hint.py`** (or an equivalent `git ls-files | wc -l`) so Phases 1–2 stay deep enough to be useful without pretending every file was read line-by-line.

## Thresholds (guidance)

Interpret the **tracked path count** from `repo_scope_hint.py` (or total file count from the walk fallback):

| Tier | Tracked paths (approx.) | Review strategy |
|------|-------------------------|-----------------|
| **Small** | ≤ 800 | Broad review feasible: follow `effective-code-review.md` across the repo with normal depth. |
| **Medium** | 801–8,000 | **Mandatory sampling:** vertical slices + security-sensitive areas + hot paths; no claim of exhaustive file-by-file review. |
| **Large** | > 8,000 | **Heavy sampling:** same as medium but narrower slices; prioritize entry points, auth/payment/data layers, and CI; explicitly list what was **not** reviewed. |

Adjust tier boundaries if the domain is unusually homogeneous (many tiny files) or concentrated (few huge packages).

## What to do in Phase 1 (map + scope)

1. Record the count and tier in the **Codebase Map** (one short subsection: “Audit scope”).
2. List **in-scope** areas (e.g. `apps/web`, `services/api`) and **out-of-scope** areas (e.g. archived packages, generated SDKs) when sampling.

## What to do in Phase 2 (audit)

1. **Vertical slice:** one end-to-end user journey through the code (see `effective-code-review.md`).
2. **Risk-weighted pass:** secrets/auth, persistence, external integrations, file uploads, parsers, permission checks.
3. **Hot files:** large modules, high churn (if git history is available), central routers or ORM layers.
4. **Explicit disclaimer** in the Audit Report summary: what was deep-reviewed vs spot-checked vs excluded.

## Reproducibility

Another run should be able to follow the same scope statement. Name directories and criteria, not vague “we looked at the important parts.”
