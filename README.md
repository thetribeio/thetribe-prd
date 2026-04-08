# codebase-audit

A [Claude Code](https://code.claude.com/docs) plugin that helps clients understand an existing codebase through a **four-phase** workflow: exploration, structured audit, functional documentation, and **optional** PDF export.

## What it does

When a client inherits, evaluates, or onboards onto an existing application, this plugin guides Claude through:

1. **Codebase exploration** — Maps repository structure, tech stack, entry points, dependencies, and configuration; records **audit scope** using repo size hints.
2. **Source code audit** — Reviews the codebase (full or **sampled** on large repos per bundled references) for architecture, security, quality, and technical debt; severity-rated report and overall health.
3. **Functional documentation** — Plain-language documentation: what the app does, data and integrations, user journeys, operations.
4. **PDF export (optional)** — Turns the three markdown sections into one PDF via **`reportlab`**, using `scripts/generate_audit_pdf.py`.

Phases 2–3 are defined entirely by this plugin’s **`references/`** files. There is **no** dependency on separate `code-review` or `documentation` skills, and Claude Code does **not** chain skills automatically—those references are the source of truth.

## Dependencies

| Phase | Requirement |
|-------|-------------|
| 1–3 | None beyond the agent and repository access. |
| 4 (PDF) | Python 3.9+ and `pip install reportlab`. |

**Fail fast before a long audit:** from `.agents/skills/codebase-audit/scripts/` run:

```bash
python check_audit_env.py --require-pdf
```

Use `--require-pdf` only when the user wants a PDF; if `reportlab` is missing, fix the environment before Phases 1–3.

**Repo sizing (Phase 1):** from the **project under audit** (repository root):

```bash
python /path/to/this/repo/.agents/skills/codebase-audit/scripts/repo_scope_hint.py
```

Then follow `.agents/skills/codebase-audit/references/large-repository-strategy.md`.

## Skills

| Skill | Trigger phrases |
|-------|-----------------|
| `codebase-audit` | "audit this codebase", "review the source code", "document this app", "give me an audit of the project" |

## Installing (Claude Code)

This repository includes **`.claude-plugin/plugin.json`** (plugin manifest) and **`.claude-plugin/marketplace.json`** (marketplace catalog with a single plugin entry).

1. Follow the official docs: [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) and [Plugins reference](https://code.claude.com/docs/en/plugins-reference).
2. Add this repository as a marketplace (per your Claude Code version’s UI or CLI, e.g. marketplace add with this **git URL**), then install the **`codebase-audit`** plugin from the **`thetribe-plugins`** marketplace.

If your Claude Code build only supports installing from a **local path**, clone this repo and use your product’s “install plugin from directory” flow pointing at the **repository root** (the folder that contains `.claude-plugin/plugin.json`).

This README does **not** use undocumented installers; if you publish elsewhere (e.g. community registries), document those steps in that channel.

## Usage

Open or `cd` into the **repository to audit**, enable the plugin, then say for example:

> "Audit this codebase and give me the functional documentation."

For markdown plus PDF, say so explicitly and ensure `check_audit_env.py --require-pdf` passes first.

Claude produces three shareable markdown sections — **Codebase Map**, **Audit Report**, and **Functional Documentation** — and can run **`scripts/generate_audit_pdf.py`** for Phase 4 when requested.
