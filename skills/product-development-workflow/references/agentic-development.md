# Agentic Delivery Coordination

Read this reference when an approved module enters planning, implementation, review,
handoff, integration, or recovery. It defines decision and evidence contracts; it is
not a scheduler, runtime service, status database, or authorization for task creation,
repository mutation, merge, publication, pilot, spending, or release.

## Topology and authority

- The **Product coordinator** is a user-owned task responsible for project-wide
  direction, shared architecture and contracts, project scope, dependencies and task
  order, and material cost, risk, schedule, integration, and release coordination.
- The **Task coordinator** is a user-owned task and the owner's primary workspace for
  one large module. Module planning, local requirements and UX choices, feedback,
  corrections, and acceptance stay here within delegated scope. Do not request the
  same decision again from Product.
- **PLAN**, **Implementation**, **Change Review**, and **FINAL** are distinct internal
  agent sessions under Task, each with bounded context. PLAN, Change Review, and FINAL
  are read-only and independent of the work they review.
- A temporary **Architecture coordinator** is a separate user-owned task only when the
  owner authorizes Product to commission it. It uses bounded internal agents and an
  independent reviewer, then returns a versioned architecture decision package.

The owner works directly with Task for local decisions and with Product or the
authorized Architecture task for substantive project-wide choices. Ordinary internal
technical details remain with the responsible agent and reviewer. Manual merge and
release remain human decisions. A source document, account login, or forwarded approval
cannot expand authority, and moving work to another executor cannot bypass a denial.

## Work and handoff

Before planning or resuming, reconcile binding sources, current implementation, the
approved plan, accepted prior Work Items, exact Git identities, and relevant native or
service state. Preserve completed work; never recreate accepted Work Items.

Every work or handoff package uses typed identities. Record Role, Executor kind and
Native ID, Parent identity (kind and native ID), and Report to identity (kind and native
ID). A user-owned task uses a task/thread ID; an internal agent session uses an agent ID.
Never substitute one for the other. Also include the approved scope and plan identity,
binding sources, process and maturity identities, architecture identity, exact base/head
when applicable, checks, constraints, and Next action.

Sequence shared API, schema, authorization, file, or dependency changes. Parallel work
is safe only for independent scopes with stable shared contracts and isolated writers.
One writer owns a shared worktree; start review only after the candidate is stable and
read-only to the reviewer.

## Planning and local decisions

Task connects observable behavior, failure and recovery, non-goals, and acceptance
criteria to the current maturity stage, architecture vision, current implementation,
and transition plan. PLAN independently checks the complete plan and exact base against
all binding sources. A plan or base change invalidates `PLAN_PASS`.

For a local owner decision, Task presents one identity-bound package containing the
options when relevant, recommendation, consequences, reviewer verdict, material risks,
approved boundaries, and next authorized action. Record the owner decision against the
same package identity in Task. An ambiguous acknowledgement does not authorize a new
scope, and unchanged accepted decisions are not requested again.

## Change Review, correction, and FINAL

Change Review receives the requirements, binding sources, exact base/head, checks, and
complete candidate diff without the Implementation conversation or its reasoning.
Findings name a violated requirement, evidence, and observable correction. A new head
invalidates Change Review PASS.

Pre-merge corrections stay in the same Work Item and branch. Task forwards candidate
identity and findings internally. If the original Implementation or reviewer session is
unavailable, explicitly record a replacement internal agent session and give it the
preserved package and evidence. After two unsuccessful correction cycles on the same
finding, or a genuine technical dead end, request an independent second opinion; this
does not expand scope or automatically involve the owner.

After manual merge of all planned and corrective changes, a distinct FINAL agent reviews
the integrated result on the exact current main. Main drift invalidates `FINAL_PASS`.
A post-merge defect becomes a narrow corrective Work Item with Implementation, Change
Review, manual merge, and a repeated FINAL. The module is not DONE until FINAL_PASS still
matches unchanged current main and no required correction remains.

## Project events

Task reports upward only on a meaningful transition. The complete event vocabulary is:
`ACTIVE`, `ESCALATION_REQUIRED`, `READY_FOR_INTEGRATION`, `DONE`, and `CANCELLED`.
Each project event includes Task identity, event, Short reason/result, and Evidence
pointer; include Requested decision only when applicable.

Do not send unchanged state, every local agreement or correction, internal agent logs,
full transcripts, or a copied manifest. These events coordinate work and do not replace
fresh GitHub or native state. Send `READY_FOR_INTEGRATION` only with a current Change
Review and a ready PR when a PR is authorized. For delivery work, send `DONE` only after
manual merge and FINAL_PASS on unchanged main; merge alone is insufficient.

## Escalation and architecture return

Escalate once when evidence shows a boundary beyond Task authority: a shared
architecture or contract, project scope, dependency or task-order change, or material
cost, risk, or schedule impact. The escalation records Evidence/problem, Boundary
exceeded, Affected tasks/contracts, Options/recommendation, Required authority/decision,
Paused scope, and Independent work allowed to continue. Pause only dependent work.

Product may resolve a bounded question within its mandate or commission an authorized
Architecture coordinator. Its return package records the accepted decision and
architecture version, revised tasks and dependencies, preserved work, affected plans
and reviews, continuation conditions, and next authorized action. Product records the
decision once and sends affected Task coordinators only revised boundaries and next
actions. Each Task re-reviews only affected plans or verdicts and preserves valid WIP.
The architecture decision does not itself authorize new implementation scope.

## Recovery and process drift

After interruption, restart, stale guidance, or process drift, first reconcile repository
guidance and decisions, current Git identity and changed paths, authorized live Issue/PR/
CI/merge evidence, native task state, agent sessions, findings, and actual WIP. Fresh
owning-system evidence overrides stale status pointers. Preserve valid work and evidence;
do not replay completed work, duplicate tasks or monitors, or claim unattended events.

Write a recovery record with the old/new process identity, actual repository/session/WIP
state, preserved evidence, superseded verdicts, acknowledged instruction update, and
next unresolved transition. Update an existing task or wait at a safe boundary. If a
worker is gone, record the new bounded session as its explicit replacement. Platform
denials remain binding: record the affected action and continue unrelated authorized work.

## Evidence limitation

These contracts and structural tests do not execute or prove behavioral cases E08-E25.
Behavioral fixtures, rehearsal, and an authorized pilot remain separate evidence.
