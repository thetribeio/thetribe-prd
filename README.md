# codebase-audit

A Claude plugin that helps clients understand an existing codebase through a structured three-phase workflow: source code exploration, code audit, and functional documentation.

## What it does

When a client inherits, evaluates, or onboards onto an existing application, this plugin guides Claude through:

1. **Codebase Exploration** — Maps the repository structure, tech stack, entry points, dependencies, and configuration.
2. **Source Code Audit** — Reviews the codebase for architecture quality, security issues, code quality, and technical debt. Produces a severity-rated report with an overall health rating.
3. **Functional Documentation** — Writes plain-language documentation covering what the app does, how data flows, key user journeys, and how to operate it.

## Skills

| Skill | Trigger |
|-------|---------|
| `codebase-audit` | "audit this codebase", "review the source code", "document this app", "give me an audit of the project" |

## Usage

Point Claude at a repository and say:

> "Audit this codebase and give me the functional documentation."

Claude will produce a self-contained report with three sections — Codebase Map, Audit Report, and Functional Documentation — each shareable with different stakeholders.
