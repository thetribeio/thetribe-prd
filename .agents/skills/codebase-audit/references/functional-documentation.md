# Functional documentation for non-technical readers

Target audience: product owners, stakeholders evaluating a buy/build decision, or new team members who are not diving into the code yet.

## Principles

- **Plain language.** Prefer “the app sends a confirmation email” over “the notification service enqueues a job”.
- **Outcome-oriented.** Describe what users achieve and what the business gains, not internal class names—except when mapping a journey to code for a mixed audience.
- **Honest scope.** Say what is in production, what is experimental, and what is unknown if the repo does not make it obvious.
- **Layered detail.** Short pitch up front; deeper sections only where they help decisions or onboarding.

## Application overview

Answer in order:

1. **What it is** — Two or three sentences: product type, primary value, and who it is for.
2. **Users and problems** — Primary personas and the jobs-to-be-done this software supports.
3. **Major capabilities** — Bullet list of features or domains (e.g. billing, admin, reporting), not file names.

Avoid implementation jargon unless the reader also needs a code map.

## Data and integrations

1. **Data the product cares about** — Entities in business terms (orders, tenants, documents), not table names unless useful for engineers reading the same doc.
2. **External systems** — APIs, payment providers, email, auth, storage; what depends on them and what happens if they fail (high level).
3. **Data flow** — One short narrative or simple diagram-in-words: where data enters, where it is stored, where it is shown or exported.

## User journeys

For **two to five** important flows:

- **Name the journey** in user language (“Sign up and first purchase”).
- **Steps** — What the user does and what they see; keep it sequential and short.
- **Code touchpoints (optional subsection)** — For handover docs: modules, services, or routes that implement each step—enough for a developer to open the right folder.

Use consistent terms across journeys (same name for the same role or object).

## Operational overview

1. **How it runs** — Hosted where, containers or serverless, background workers if any.
2. **Configuration** — Categories of settings (secrets, feature flags, URLs)—not secret values.
3. **Monitoring** — How operators know it is healthy; where logs and alerts live, if discernible from the repo or runbooks.

If deployment is unclear from the repository, say so and list what is missing (e.g. no Dockerfile in tree).

## Style and structure

- Short paragraphs and bullets; **bold** sparingly for terms you want skimmable.
- **Do not** paste large config dumps or stack traces into functional docs; summarize or link to runbooks.
- Keep the same section order as the audit deliverable so the PDF and markdown stay aligned: Overview → Data & integrations → User journeys → Operations.
