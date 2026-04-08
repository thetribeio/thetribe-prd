---
name: codebase-audit
description: >
  Explores an existing codebase, produces a structured source code audit, and writes functional documentation for the application.
  Trigger with "audit this codebase", "review the source code", "document this app", "give me an audit of the project",
  or when a client needs to understand an existing application they've inherited or are evaluating.
  Optional PDF export (Phase 4) needs Python and reportlab—run scripts/check_audit_env.py --require-pdf before Phases 1–3 if PDF is required.
---

# Codebase Audit & Functional Documentation

End-to-end workflow to onboard a user (developer/product owner) onto an existing codebase: map the source code, produce a structured audit, write functional documentation, and **optionally** export a PDF.

Bundled **`references/`** define how to review and document (Phases 2–3). **`scripts/`** supports environment checks, repo sizing, and PDF generation (Phase 4).

## Pre-flight (before Phase 1)

Do this **first** so users are not surprised after a long run.

1. **Clarify deliverables** — Confirm whether the client wants **markdown only** or **markdown + PDF**. There is **no native skill-to-skill chaining** in Claude Code: Phases 2–3 are driven only by this skill’s **`references/`** files, not by other installed skills. If the user has extra skills (e.g. a personal code-review skill), they may influence style, but **reproducibility** comes from following the references below.

2. **PDF (Phase 4) — fail fast** — If a PDF is required, run from this skill’s `scripts/` directory:

   ```bash
   python check_audit_env.py --require-pdf
   ```

   If this exits non-zero, **stop** and tell the user to run `pip install reportlab` (Python 3.9+) before continuing. Do **not** rely on YAML `compatibility` metadata (it is not part of the official skill frontmatter schema and may be ignored).

3. **Repository size** — From the **repository root** of the project under audit, run:

   ```bash
   python repo_scope_hint.py
   ```

   Map the printed count to a **tier** and sampling plan in **`references/large-repository-strategy.md`**. Record the tier and scope in the **Codebase Map** before deep reading.

## Phase 1 — Codebase Exploration

Map the repository before drawing any conclusions.

- Identify the language(s), framework(s), and runtime environment
- List top-level directories and explain the role of each
- Locate entry points (main files, server bootstrap, CLI entrypoints)
- Identify the dependency manifest(s) and note key dependencies and their versions
- Check for configuration files (env files, CI/CD pipelines, Docker, infra-as-code)
- Note the test setup: framework, coverage, test types present
- **Scope:** apply **`references/large-repository-strategy.md`** using the count from **`scripts/repo_scope_hint.py`** (or equivalent). Do **not** claim a full line-by-line review of every file on large repositories; state what was reviewed deeply vs sampled.

Output a **Codebase Map** section with a directory tree and a one-line description per folder, plus a short **Audit scope** note (tier + sampling approach).

## Phase 2 — Source Code Audit

Perform the audit **using only** **`references/effective-code-review.md`** for methodology (plus **`references/large-repository-strategy.md`** for scope on medium/large repos). **Do not** assume separate `code-review` or `documentation` skills exist; they are not bundled with this plugin.

Review breadth must match the scope from Phase 1 (full where small; sampled where medium/large). Focus on:

### Architecture & Structure
- Is the architecture consistent and intentional (layered, hexagonal, MVC, etc.)?
- Is responsibility well separated? Are there god objects or god modules?
- Is there meaningful abstraction, or is there over-engineering / under-engineering?

### Security
- Hard-coded secrets or credentials
- Insecure data handling (auth, input validation, SQL injection, XSS, CSRF)
- Dependency vulnerabilities (flag obviously outdated or known-CVE packages)

### Code Quality
- Naming clarity and consistency
- Dead code, commented-out blocks, TODOs
- Error handling: are errors surfaced, swallowed, or ignored?
- Test coverage: what is tested, what is not

### Technical Debt
- Duplicated logic that should be unified
- Deprecated patterns or libraries
- Missing documentation for non-obvious logic

Output an **Audit Report** section structured as:
1. Summary (3–5 sentences, overall health; **include explicit review scope** if sampling was used)
2. Critical findings (must fix before production or handover)
3. Significant findings (should fix soon)
4. Minor findings (nice to have)
5. Positive observations

Rate overall health as: `Good` / `Needs Improvement` / `Requires Significant Work`.

## Phase 3 — Functional Documentation

Produce documentation for a **non-technical or semi-technical audience** (product owners, new team members, evaluating clients). Follow **`references/functional-documentation.md`** only—there is no dependency on an external `documentation` skill.

**Application Overview**
- What does this application do? (2–3 sentence pitch)
- Who are the users and what problems does it solve?
- What are the main functional modules or features?

**Data & Integrations**
- What data does the application manage?
- What external services, APIs, or databases does it connect to?
- What does data flow look like at a high level?

**User Journeys**
- Describe 2–5 key user flows through the application in plain language
- Map each flow to the code modules that support it

**Operational Overview**
- How is the application deployed and run?
- What configuration is required?
- How is it monitored or observed?

## Output Structure

Deliver results in this order:

```
## Codebase Map
[directory tree + descriptions]

## Audit Report
[summary, findings by severity, positive observations]

## Functional Documentation
[overview, data & integrations, user journeys, operational overview]
```

Keep each section self-contained so the client can share individual sections with different stakeholders.

## Phase 4 — PDF Export (optional)

**Requires** Python 3.9+ and **`pip install reportlab`**. Re-check any time before generating:

```bash
python check_audit_env.py --require-pdf
```

Once all three markdown sections are complete, save the full report (in delivery order: Codebase Map, Audit Report, Functional Documentation) to a `.md` file and run:

```bash
python /path/to/codebase-audit/scripts/generate_audit_pdf.py \
  --input path/to/audit-report.md \
  --title "Application Name" \
  --author "Author or team" \
  --date YYYY-MM-DD \
  --output path/to/application-name-audit-YYYY-MM-DD.pdf
```

`--output` is optional; default is `<slug(title)>-audit-<date>.pdf` next to the input file.

The script lives at **`scripts/generate_audit_pdf.py`**. It produces:

- Title page (application name, audit date, author)
- Table of contents with page references for each main section
- One chapter per `## Codebase Map`, `## Audit Report`, and `## Functional Documentation` block

Styling (colors, typography, markdown subset, and ReportLab implementation details) is defined in the script so exports stay consistent—adjust there if the palette or rules change.
