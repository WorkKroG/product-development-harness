# Work Item and Review Templates

Copy only the needed record into the project's approved evidence location. Replace each
placeholder with a portable identity or `Unknown`. Runtime observations belong in the
current handoff, not this asset.

Identity values are typed pairs. A user-owned coordinator uses kind `user-owned task`
and a task/thread ID; an internal worker uses kind `internal agent session` and an agent
ID. Never pass an agent ID to a user-owned task API or a task/thread ID to an internal
agent API. A queued client ID is provisional, not a usable Native ID.

## Work package / handoff

- Work Item/module identity: `<stable identity>`
- Outcome/why: `<observable result and reason>`
- Scope/non-goals: `<included and excluded work>`
- Binding sources: `<authoritative artifacts and identities>`
- Dependencies: `<ordering and stable shared contracts>`
- Maturity identity: `<current and target stage>`
- Architecture identity: `<decision version and implementation boundary>`
- Process identity: `<selected workflow release, commit, or content identity>`
- Plan identity: `<version and content hash>`
- Exact base: `<full Git identity or not applicable>`
- Exact head: `<full Git identity, pending, or not applicable>`
- Allowed paths: `<complete bounded path set>`
- Permissions/data/recovery: `<authority, access, lifecycle, failure, resume>`
- Acceptance criteria: `<observable criteria>`
- Checks: `<required fresh checks>`
- Role: `<Product, Task, PLAN, Implementation, Change Review, FINAL, Architecture>`
- Executor kind: `<user-owned task or internal agent session>`
- Native ID: `<task/thread ID or agent ID of that kind>`
- Parent identity: `<kind and native ID>`
- Report to identity: `<kind and native ID>`
- Constraints: `<non-bypass and other boundaries>`
- Current state/findings: `<evidence-backed state>`
- Next action: `<one unresolved transition>`

## Review record

- Phase: `<PLAN, Change Review, or FINAL>`
- Independent reviewer kind: `<internal agent session>`
- Independent reviewer Native ID: `<agent ID>`
- Reviewed plan hash or base/head/main: `<exact identity required by phase>`
- Binding sources: `<complete identified set>`
- Checks: `<fresh results and environment>`
- Findings: `<violated requirement, evidence, observable correction; or none>`
- Verdict: `<PLAN_PASS, PASS, FINAL_PASS, or changes required>`
- Invalidation condition: `<plan/base change, new head, or main drift>`

PLAN review binds to plan content hash and exact base. Change Review binds to exact base
and head and records the complete changed-path set and full-diff inspection. FINAL binds
to exact current main and the complete set of integrated planned/corrective Work Items.

## Local decision

- Package identity: `<version or content hash>`
- Decision authority and location: `<owner/delegate and Task or Architecture task>`
- Outcome/why: `<decision and reason now>`
- Scope/non-goals: `<included and excluded consequences>`
- Options/recommendation: `<meaningful options and recommended choice>`
- Consequences and material risks: `<decision-bearing effects>`
- Reviewer verdict: `<verdict and reviewed identity>`
- Owner decision: `<decision bound to Package identity>`
- Approved boundaries: `<scope and residual-risk limits>`
- Next authorized action: `<precise action enabled>`

## Project event

- Task identity: `<kind and native ID>`
- Event: `<ACTIVE | ESCALATION_REQUIRED | READY_FOR_INTEGRATION | DONE | CANCELLED>`
- Short reason/result: `<one concise transition statement>`
- Evidence pointer: `<owning-system or versioned evidence>`
- Requested decision: `<only when applicable; otherwise omit>`

Send only changed project state, never unchanged progress, full transcripts, internal
logs, every local correction, or a duplicate live-status database. READY_FOR_INTEGRATION
requires a current Change Review and ready PR when authorized. Delivery DONE requires
manual merge and FINAL_PASS on unchanged main.

## Escalation

- Evidence/problem: `<facts and evidence pointer>`
- Boundary exceeded: `<shared contract, scope, dependency/order, cost/risk/schedule>`
- Affected tasks/contracts: `<bounded impact>`
- Options/recommendation: `<options and recommended response>`
- Required authority/decision: `<Product or substantive owner decision>`
- Paused scope: `<dependent work only>`
- Independent work allowed to continue: `<safe authorized work>`
- Next action: `<one resolution step>`

## Architecture return

- Accepted decision/architecture version: `<versioned decision identity>`
- Revised tasks/dependencies: `<affected decomposition and ordering>`
- Preserved work: `<valid WIP and evidence>`
- Affected plans/reviews: `<items requiring renewed review>`
- Continuation conditions: `<conditions to resume dependent work>`
- Next authorized action: `<bounded action>`

## Recovery

- Old process identity: `<previous instruction identity>`
- New process identity: `<current instruction identity>`
- Actual repository/session/WIP state: `<fresh Git, service, task, agent, and WIP facts>`
- Preserved evidence: `<still-valid immutable evidence>`
- Superseded verdicts: `<identity drift and invalidated verdicts>`
- Acknowledged instruction update: `<task/session acknowledgement evidence>`
- Replacement session: `<old/new Executor kind and Native ID, if required>`
- Next unresolved transition: `<first incomplete transition>`

## Platform denial

- Attempted action and purpose: `<exact action and dependent outcome>`
- Denial or constraint: `<observed platform result>`
- Dependent scope: `<blocked action only>`
- Independent work allowed to continue: `<safe authorized work>`
- Required owner or platform next action: `<precise resolution>`
- Preserved WIP/evidence: `<identity and location>`

## Evidence limitation

These templates and their structural checks do not execute behavioral cases E08-E25.
Fixtures, rehearsal, and any authorized pilot are separate evidence.
