# codebase-audit

A Claude plugin that helps clients understand an existing codebase through a structured four-phase workflow: source code exploration, code audit, functional documentation, and PDF export.

## What it does

When a client inherits, evaluates, or onboards onto an existing application, this plugin guides Claude through:

1. **Codebase Exploration** — Maps the repository structure, tech stack, entry points, dependencies, and configuration.
2. **Source Code Audit** — Reviews the codebase for architecture quality, security issues, code quality, and technical debt. Produces a severity-rated report with an overall health rating.
3. **Functional Documentation** — Writes plain-language documentation covering what the app does, how data flows, key user journeys, and how to operate it.
4. **PDF Export** — Compiles the full report into a PDF file for handoff to the client.

## Requirements

- The `pdf` skill must be installed for the PDF export phase to work.
- If `pdf` is not available, the first three phases can still be completed but the final PDF export will fail.

## Installation

This repository includes a Claude Code marketplace manifest in `.claude-plugin/marketplace.json`.

The `/plugin marketplace add` and `/plugin install` flow should be validated against the published repository state before being documented as the standard installation path for users.

## Skills

| Skill | Trigger |
|-------|---------|
| `codebase-audit` | "audit this codebase", "review the source code", "document this app", "give me an audit of the project" |

## Usage

Point Claude at a repository and say:

> "Audit this codebase and give me the functional documentation."

Claude will produce a self-contained report with three core sections — Codebase Map, Audit Report, and Functional Documentation — then export the result as a PDF when the `pdf` skill is available.
