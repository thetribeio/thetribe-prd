---
name: codebase-audit
description: >
  Explores an existing codebase, produces a structured source code audit, and writes functional documentation for the application.
  Trigger with "audit this codebase", "review the source code", "document this app", "give me an audit of the project",
  or when a client needs to understand an existing application they've inherited or are evaluating.
compatibility: "Requires the pdf skill from anthropics/skills (install with: claude skills add anthropics/skills/pdf)"
---

# Codebase Audit & Functional Documentation

End-to-end workflow to onboard a client onto an existing codebase: map the source code, produce a structured audit, and write functional documentation for the application.

## Phase 1 — Codebase Exploration

Map the repository before drawing any conclusions.

- Identify the language(s), framework(s), and runtime environment
- List top-level directories and explain the role of each
- Locate entry points (main files, server bootstrap, CLI entrypoints)
- Identify the dependency manifest(s) and note key dependencies and their versions
- Check for configuration files (env files, CI/CD pipelines, Docker, infra-as-code)
- Note the test setup: framework, coverage, test types present

Output a **Codebase Map** section with a directory tree and a one-line description per folder.

## Phase 2 — Source Code Audit

Review the full codebase (not just a diff) using the `code-review` skill. Focus on:

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
1. Summary (3–5 sentences, overall health)
2. Critical findings (must fix before production or handover)
3. Significant findings (should fix soon)
4. Minor findings (nice to have)
5. Positive observations

Rate overall health as: `Good` / `Needs Improvement` / `Requires Significant Work`.

## Phase 3 — Functional Documentation

Use the `documentation` skill to produce documentation for a **non-technical or semi-technical audience** (product owners, new team members, evaluating clients).

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

## Phase 4 — PDF Export

Once all three sections are complete, use the `pdf` skill to compile the full report into a single PDF file using `reportlab`.

### Structure

- Title page: application name, audit date, and author
- Table of contents with page references to each section
- Each section (Codebase Map, Audit Report, Functional Documentation) as a separate chapter

### Color palette

Define these constants at the top of the generation script:

```python
PRIMARY   = HexColor('#334bec')   # headings, highlights, links
SECONDARY = HexColor('#1f2e9a')   # code block backgrounds (darker shade of primary)
```

### Typography and styles

Use `reportlab.platypus` (`SimpleDocTemplate`, `Paragraph`, `Preformatted`, `Table`) with these style rules:

- **Headings** (`Heading1`, `Heading2`, `Heading3`): set `textColor = PRIMARY`
- **Inline code** (text between backticks): render as `<font name="Courier" color="#1f2e9a">…</font>` inside a `Paragraph`. Never omit or strip backtick-delimited text — it must always be visible.
- **Code blocks** (fenced with triple backticks): render with `Preformatted` using:
  - `fontName = 'Courier'`
  - `fontSize = 8`
  - `textColor = white`
  - Wrap inside a `Table` with a single cell, `backColor = SECONDARY`, and 6 pt padding on all sides
- **Body text**: black on white, `fontSize = 10`

### Markdown-to-reportlab conversion rules

Before building the story, parse the markdown content and apply these conversions in order:

1. Fenced code blocks (` ``` … ``` `) → `Preformatted` wrapped in a colored `Table` (see above)
2. Inline code (`` `…` ``) → `<font name="Courier" color="#1f2e9a">…</font>` inside a `Paragraph`
3. `**bold**` → `<b>…</b>`
4. `# Heading` levels → `Paragraph` with the corresponding `Heading` style
5. Bullet lines (`- …`) → `Paragraph` with `styles['Bullet']`
6. Plain text → `Paragraph` with `styles['Normal']`

Never use Unicode subscript/superscript characters — use ReportLab's `<sub>` and `<super>` tags instead.

Name the output file `<project-name>-audit-<YYYY-MM-DD>.pdf` and deliver it to the client.
