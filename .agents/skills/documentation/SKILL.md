---
name: documentation
description: >
  Write functional and technical documentation for an existing application.
  Use when the user asks for onboarding material, system explanation, architecture documentation,
  feature documentation, or when another skill needs clear documentation for a non-technical or
  semi-technical audience.
---

# Documentation

Write documentation that helps someone understand what the application does, how it works at a high level, and how it is operated.

## Audience

Default to a non-technical or semi-technical audience:

- Product owners
- New team members
- Evaluating clients
- Stakeholders who need a clear system overview

Adjust the level of detail so the document stays understandable without becoming vague.

## Writing Principles

- Explain the purpose of the application before the implementation details.
- Prefer user flows and business functions over file-by-file descriptions.
- Explain why a module matters, not just that it exists.
- Keep technical jargon limited and define it when needed.
- Stay concrete: use the actual features, data, and integrations found in the codebase.
- Keep the documentation self-contained and easy to share.

## What to Cover

### Application Overview

- What does the application do?
- Who uses it?
- What problem does it solve?
- What are the main functional modules or features?

### Data and Integrations

- What data does the application manage?
- What external systems, APIs, databases, or services does it depend on?
- What does the high-level data flow look like?

### User Journeys

- Describe 2 to 5 important user flows in plain language.
- Connect each flow to the main modules that support it.
- Focus on what the user is trying to accomplish and what the system does in response.

### Operational Overview

- How is the application run or deployed?
- What configuration or infrastructure matters?
- What testing, monitoring, logging, or observability signals are visible?

## Output Format

Write the result using this structure:

```markdown
## Functional Documentation

### Application Overview
[clear explanation]

### Data & Integrations
[clear explanation]

### User Journeys
1. [journey]
2. [journey]

### Operational Overview
[clear explanation]
```

## Documentation Rules

- Do not turn the document into a directory listing.
- Do not assume the audience already knows the stack.
- Do not invent product intent that is not supported by the codebase.
- If something is uncertain, state the uncertainty briefly instead of guessing.
- Prefer clear prose over exhaustive technical detail.
- Keep the result useful as a handoff or evaluation document.
