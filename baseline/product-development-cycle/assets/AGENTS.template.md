# Project Agent Operating Guide

## Mission

Develop this product through evidence-based lifecycle gates. Start major work with `$product-development-cycle`, preserve existing decisions, and continue from the first incomplete gate.

The globally installed `$product-development-cycle` skill is the canonical pipeline. Do not copy its complete instructions into this repository. Record only project-specific commands, sources of truth, status, decisions, and explicit exceptions here.

## Sources Of Truth

- Current status: `docs/PROJECT_STATUS.md`
- Product requirements: `<path>`
- User journey and story map: `<path>`
- Design: `<path or Figma URL>`
- Architecture and decisions: `<path>`
- Backlog: `<path>`
- Risks and release checklist: `<path>`

Update existing authoritative artifacts. Do not create competing versions of the same document.

## Commands

- Install: `<command>`
- Develop: `<command>`
- Test: `<command>`
- Lint: `<command>`
- Type check: `<command>`
- Build: `<command>`
- Migrate: `<command>`

Discover missing commands from the repository before changing code.

## Lifecycle Rules

- Do not silently skip a product gate. Record the reason, risk, owner, and revisit condition.
- Separate evidence, assumptions, open questions, decisions, and non-goals.
- Cover happy, alternate, failure, recovery, permission, and data-lifecycle paths.
- Require explicit product-owner approval at scope, design, architecture/risk, and release gates.
- Do not begin broad implementation without testable acceptance criteria and an approved technical plan.

## Delivery Protocol

- One backlog item per small branch or worktree; use `codex/<id>-<description>` unless the repository specifies otherwise.
- Keep edits scoped and preserve unrelated user changes.
- Add tests proportional to behavior and risk.
- Run fresh relevant tests, lint, type checks, build, and migrations before declaring completion.
- Require independent review where practical; the builder is not the sole approver.
- Add security review for auth, permissions, secrets, input, data exposure, dependencies, and infrastructure.
- Add UX and accessibility review for user-facing changes.

## Parallel Work

Parallelize only independent tasks with stable contracts and clear file ownership. Coordinate product documents, shared contracts, auth, schema migrations, integration, and release sequentially.

## Completion

Report changed artifacts, verification evidence, unresolved risks, and the next lifecycle gate. Do not call work release-ready while a required gate remains unmet.
