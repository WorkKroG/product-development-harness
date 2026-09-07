# Product Development Workflow — operating guide

## Mission and authority

Develop the original `product-development-cycle` as the renamed Codex-only
`product-development-workflow` skill and Product Development Workflow product.
Start or resume major work with `$product-development-workflow`, preserving the decisions
in README.md and SPEC.md. This repository develops the skill itself: the installed global
copy and `baseline/` are historical inputs, not permission to overwrite the agreed process.
The owner's explicit staged-development decisions take precedence over conflicting legacy
requirements, including the old heavy Gate 4.5 and mandatory detailed early finance.

## Sources and current step

- `docs/PROJECT_STATUS.md`: current stage and next action.
- `SPEC.md`: proposed target behavior and accepted principles; remaining proposals stay explicit.
- `AUDIT.md`: A01–A24 findings to resolve.
- `EVALUATION.md`: E01–E41 proposed behavior checks, not executed evidence.
- `SOURCES.md`: public provenance summary; `BASELINE.sha256`: original skill identity.
- `HANDOFF.md`: coordinator context. `.local-handoff/` is ignored private historical evidence;
  it must never become active instructions or public repository content.

Bootstrap is authorized: preserve the exact baseline in a first local commit and the
prepared specification/project instructions in a second local commit. These seed commits
contain documentation only. Subsequent implementation uses isolated `codex/` branches/worktrees.
The current task is the approved naming/coordination amendment and revised Module 3 plan.
Historical bootstrap and module plans do not override newer owner decisions in SPEC.md.
No global skill installation, public push, release, or automatic merge is authorized by bootstrap.

## Decisions and coordination

The Product coordinator owns project-wide direction, shared architecture and cross-module decisions.
The owner works directly with each Task coordinator on the module plan, local product decisions,
implementation feedback and acceptance within the delegated scope. Do not route these approvals
through Product again. Preserve consequential decisions in versioned artifacts for recovery.
Do not ask the owner to approve ordinary internal technical details or relay completion messages.
Do not ask again for unchanged decisions already captured in the approved scope.
Each large module gets one user-owned Task coordinator task. PLAN, Implementation, Change Review
and FINAL run as distinct internal subagents with bounded context, under that coordinator.
Reviewers receive the requirements and candidate independently of the author's conversation.
Review the exact current
head; further commits invalidate the previous recommendation. Corrections after module review
follow the same change/review process. Merge remains manual.
The owner approved this topology on 2026-09-07. Existing held implementation/review tasks retain
their WIP and evidence; migrate only after a reviewed replacement plan, not as a denial bypass.
Create additional user-owned coordinator/architecture tasks only under user authorization.
Report upward only ACTIVE, ESCALATION_REQUIRED, READY_FOR_INTEGRATION, DONE or CANCELLED
transitions, with a short reason and evidence pointer; no unchanged updates or full transcripts.
Escalate changes to shared architecture/contracts, project scope, dependencies, task sequencing,
or material cost/risk/schedule. Pause only affected work. Product may resolve a bounded issue or
commission an authorized architecture task with subagents. It then records the decision and sends
revised boundaries to affected tasks. Material owner choices and manual release/merge stay human.
Parallel work needs independent scope and stable shared contracts. Route material scope/cost/risk
changes and release decisions to the main coordinator. Respect platform denials; never bypass them
by switching tools, credentials, or executor. Continue unrelated authorized work.

## Models

Use native model/reasoning fields and verify availability; never silently substitute:

| Stage | Model / reasoning |
|---|---|
| Product/Task coordination, decomposition, PLAN review | gpt-5.6-sol / high |
| Ordinary implementation and bugfix | gpt-5.6-sol / medium |
| Small obvious low-risk change, trial | gpt-5.6-terra / medium |
| Complex debugging | gpt-5.6-sol / high; escalation gpt-6-astra / high |
| Change Review | gpt-5.6-sol / high |
| Substantial architecture, security review, FINAL, second opinion | gpt-6-astra / high |

## GitHub and verification

GitHub host: `github.com`. Repository: `WorkKroG/product-development-harness` (public).
Use `gh` as the sole GitHub service client, with explicit host/repository and a bounded
authenticated read check before the first service action. Discover the installed executable
without reading tokens. Git handles fetch, local commits and separately authorized push.
Do not use GitHub browser/UI, `gh browse`, `--web`, or alternative service transports as fallback.
Before branching/review, fetch and record immutable SHAs where evidence is required.
GitHub owns Issue/PR/CI/merge state; documents must not duplicate a live status database.

The original private package is retained only in ignored `.local-handoff/`. Do not force-add it,
publish private source links/IDs, or invent a license for original/external skill materials.
Review publication scope and provenance before the first public push.

Current check: `shasum -a 256 -c BASELINE.sha256` verifies the preserved seven-file baseline.
The active skill has a Python contract suite (`python3 -B -m unittest discover -s tests -v`),
but no runtime harness or executed behavioral pilot. Discover/add only checks justified
by the actual change. Use `skill-creator` for skill implementation and the applicable planning,
review and verification skills. Add behavior checks proportional to risk; link checks alone do
not prove that coordination or lifecycle behavior works. Preserve test evidence and limitations.
