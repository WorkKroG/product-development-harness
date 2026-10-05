# Product Development Workflow v0.1 — Draft Specification

Owner decision of 2026-09-07: the product is **Product Development Workflow**, the active skill is
`product-development-workflow`, invoked as `$product-development-workflow`. This renames the
`product-development-cycle` under development; it does not create a second parallel skill. This
decision does not change the historical baseline, the globally installed copy, or the GitHub
repository address. On the same day, autonomous Task coordinators with internal subagents and
event-driven escalation (§§6–8) were approved. These decisions supersede the conflicting topology
in older plans; implementing the protocol requires an updated Module 3 PLAN review.

Status: the architectural package for the first working version, `FWP-PLAN-v1`, was approved by
the owner on 2026-09-06. The lifecycle core and profile/runtime have already been implemented; the
accepted baseline context and next step are in [PROJECT_STATUS.md](PROJECT_STATUS.md). Module 3 is
undergoing plan review in light of the 2026-09-07 decisions; completed modules must not be recreated.
The project was created with the owner's authorization on 2026-09-06; the public repository is
`WorkKroG/product-development-harness`. Plan preparation is authorized; the proposals for the
Markdown profile, FWP contents, status/navigation updates, early-role models, dependencies, and a
synthetic pilot were approved as part of `FWP-PLAN-v1`. Public distribution remains a separate
decision. Clarification of 2026-09-06: the owner approved the architectural vision for future scale,
incremental implementation, and review of decisions before scaling. The remainder of the
specification retains its proposal status; this approval does not authorize creating a remote or
publishing. A lightweight assessment of market, competition, and economics between Positioning and
Journey was also approved. Basis: [audit](AUDIT.md), [sources](SOURCES.md).

## 1. Problem and user

The owner of several products wants to start and continue development in Codex using one
reproducible process. The owner makes substantive product decisions and performs merges, but does
not manually relay results between tasks or approve every technical detail.

Product Development Workflow evolves the existing product-development-cycle. It combines lifecycle
instructions, role workflows, context templates, evidence rules, and small checks. Codex and the
existing Git/GitHub tools provide execution.

Practical outcome: from a product description and the available artifacts, a new Product
coordinator identifies the next stage, requests only missing decisions, organizes authorized work,
and returns to the owner at the right moment.

Core principle: design for future scale, implement architecture
gradually and before expansion, revise decisions based on accumulated data.
The future architectural vision is not a task to implement the entire infrastructure at once.

## 2. First-version scope

Included:

- Codex desktop as the first tested environment; The availability of specific tools is checked.
- A new product, resumption, audit of an existing product, standalone module, and release preparation.
- Full semantic cycle of the original skill, including discovery, economics, UX, risk and feedback.
- Five stages of product development with architectural vision, ongoing implementation
  and a revised plan for moving to the next scale.
- Two levels of user chats: project and large task; local agreements within
  task, general project issues through Product coordinator, execution and review by subagents.
- GitHub as Issue/PR/CI status source, gh as the only GitHub service client.
- Local installation of a specific version and safe update of projects already using it.
- A small anonymized pilot and a set of behavioral scenarios.

Not included:

- Own scheduler/server, lifecycle state database, dashboard and universal plugin marketplace.
- Support for other agent environments, separate guarantee of CLI/cloud coordination.
- Bypassing the sandbox or automated action checks, or eliminating human involvement in every external action.
- Automatic merge/release, purchasing resources or changing account permissions.
- New universal application stack or copy of the Recipes implementation.
- Copying all installed third-party skills to the distribution.

Public distribution and plugin packaging may come later; for personal Codex v0.1, a repository,
an installable skill, and a verified installation method are sufficient.

## 3. Source of truth and structure
Proposed structure of the future repository:

    README.md launch, installation, update, support limits
    CHANGELOG.md changes affecting workflow users
    skills/product-development-workflow/
      SKILL.md existing entry point, short routing
      agents/openai.yaml existing UI metadata
      references/
        lifecycle.md gate 0–16 and 3.5, stages and transitions of architecture
        quality-gates.md criteria and scenario matrix
        financial-model.md lightweight assessment 3.5 and refinement of economics in Gate 8
        agentic-development.md roles, handoffs, review, restoration
        codex-runtime.md native capability and GitHub access
        dependencies.md required skills, fallback and blocking conditions
      assets/
        AGENTS.template.md
        project-profile.template.md
        PROJECT_STATUS.template.md
        role-prompts.md
        work-item-and-review-templates.md
      scripts/ justified mechanical checks
    tests/
      fixtures/ synthetic projects and events
      scenarios.md human behavior category
    docs/
      design.md approved workflow specification
      validation.md actual pilot results

The scripts/fixtures folders are filled when specific checks are implemented, not with empty scaffolds.
Do not create a file for each small rule if the existing reference is sufficient.
README/CHANGELOG refer to the distribution repository; do not duplicate them within each product.

The workflow repository owns a version of the common rules. The product repository owns the requirements,
decisions, evidence, and its settings. The installed skill copy delivers the selected version; it
is not an independent source of development. The full lifecycle is not copied into products.

GitHub owns the latest Issue/PR/CI/merge data; local documents store requirements,
navigation, decisions made and links. Do not maintain a second constantly synchronized CI table.

## 4. Startup, version, and project settings

The active invocation is `$product-development-workflow`. The old name refers to the baseline and
the not-yet-updated globally installed copy; this change does not create a compatibility alias.
At startup, the coordinator:

1. Determines the intent: start, resume, audit, module, or release. Discovering the skill itself
   does not authorize project changes or creation of external entities.
2. Reads AGENTS, existing artifact map and facts; recognizes existing document names.
3. Checks the selected workflow version and the availability of the capabilities of the current stage.
4. Determines the current/target product stage and finds the first missing or
   refuted gate in its scope; gives the result and one next step.
5. Creates/updates minimal artifacts only in the permitted area and as needed.

The product profile is a small Markdown with validated fields and a link from AGENTS.
v0.1 does not require a separate DSL, YAML configurator or generated AGENTS:

- process release and commit/content identity;
- product mode and goal, language of communication, sources of requirements and owner decisions;
- current/target stage of development, architectural vision and immediate transition plan;
- load profile with units of measurement, assumptions, checks and cost constraints;
- GitHub host/repository, available local commands;
- roles and exact model/reasoning values;
- allowed parallelism and real dependencies;
- commercial assumptions/goals or non-commercial budget/value constraint;
- options for applicability of UX/security/release checks.

Unknown values are marked as unknown and resolved before a dependent action.
Until the problem is analyzed, the unknown deploy target does not block the investigation.
Absolute paths of executables, current task IDs and short access-check results refer to
to the runtime handoff; do not embed personal-machine data in shared templates.

The product saves a specific version. When the installed copy changes, the coordinator shows
divergence and stops only dependent transitions until a consistent version selection is made.
The first installation method is a documented copy of a specific release/commit in reality
supported discovery location, with a check to see which skill is available to Codex.
A symlink to a moving working branch does not count as version pinning.

Don't keep two indistinguishable active versions of the same skill and don't assume automatic
merging instructions. Check installation paths in the target environment using
[official documentation](https://learn.chatgpt.com/docs/build-skills).
Do not change the shared installed skill silently: it may serve other products.

## 5. Lifecycle

We retain the numbering of the original skill's main stages. We replace the old Gate 4.5 with a
lightweight Gate 3.5 before Journey and correct the internal A14/A15 discrepancies.
Depth matches the decision and product; evidence closes a gate, not the presence of a completed file.
Gate and stage of development are different coordinates. The map below applies to the current scope:
the research prototype is not required to cover public launch requirements in advance.
Future requirements are maintained in the architectural vision and transition plan with explicit status.

| Gate | Result | Responsibility and Transition |
|---|---|---|
| 0 Context | Map of facts, artifacts, contradictions and possibilities | Product coordinator selects the next open gate |
| 1 Problem | Problem, available evidence, hypotheses and test method | Owner accepts problem/success via Product coordinator |
| 2 Users | Actors, situations and jobs | PM/research role; significant changes are returned owner |
| 3 Positioning | Alternatives, audience and value; or justified inapplicability | Matches external/internal product |
| 3.5 Viability — lightweight assessment | Estimate of accessible market, competition, revenue/costs, and key unknowns | Through the Product coordinator, the owner decides whether to continue, test the hypothesis with a small experiment, change the idea, or stop |
| 4 Journey | Main path, errors, recovery, rights and return | Testable behavior, not a list of screens |
| 5 Scope | Vertical MVP and non-goals | Owner states scope |
| 6 PRD | Testable requirements and acceptance criteria | PM prepares an artifact linked to the journey |
| 7 Challenge | Independent PRD review; critical issues resolved | Owner approves meaningful result after challenge |
| 8 Finance | Clarification of rating 3.5 taking into account scope/PRD; sufficient depth for next investment | Finance capability; owner makes a decision without repeating the unchanged study |
| 9 UX | Flows and states, responsiveness/accessibility by applicability | UX role and review; owner asserts conceptual behavior |
| 10 Risk | Rights, data, threats and measures; residual risks | Security role; new scope/cost return to the corresponding gate |
| 11 Technical plan | Architecture/Data/API/Operations for Product | Technical specialists and independent review; owner sees the consequences |
| 12 Delivery plan | Top-level modules and dependencies | Entering the sequence of reviewed and owner-approved module plans |
| 13 Implementation | Small verified Work Items | Implementation/Change Review under Task coordinator |
| 14 Verification | Collaborative behavior, required checks, real manual checks | Whole-Task and release evidence, not replacing CI with a whole set of checks |
| 15 Release | Prepared rollout/rollback/monitoring/support | Owner authorizes a specific release; result and recovery are checked |
| 16 Learn | Results, feedback, updated hypotheses/economics | Return to the first affected gate |

### 5.1. Five stages of product development

| Stage | Verifiable outcome | Architectural work |
|---|---|---|
| Working prototype | You can go through the main scenario manually and test the hypothesis | Early assessment of key constraints and future pressures; minimal working implementation, explicit stubs and testing boundaries |
| MVP / first limited test | Real test users get the main result, the team collects feedback | Simple structure with clear boundaries and data changes; necessary protection, recovery and updating; further growth path outlined |
| Scale 1 - benchmark 10 thousand users | Target scenario operates under consistent load and cost profile | Checking capacity and reliability, eliminating confirmed limitations, clarifying the next transition |
| Scale 2 - benchmark 100 thousand users | Product withstands specified peaks, data volume and operating conditions | Reconsidering early assumptions; justified changes to components, storage and operation with safe migration |
| Scale 3 — mature operations | Accepted reliability, recovery, support, and cost targets are confirmed | The architecture and operations match actual product requirements; changes and emergency scenarios are verifiable |

The numbers 10/100 thousand are product guidelines, not universal technical standards.
For each product, you need to determine which users we are talking about: registered,
active for a period or simultaneously working. From this, queries/operations in peak are derived,
data volume, difficult scenarios, acceptable latency and budget. Without this data it is impossible
declare the architecture ready for the specified scale.

Quality is also determined by the type of data and the consequence of failure. As soon as they appear
real data and external users, we need appropriate rights, security and
restoration; they cannot be postponed until the fifth stage just because of the small number of users.
Mature operation requirements may be needed earlier for a particular risk.
Progressing through the steps does not require rewriting the product or mechanically adding technology.

### 5.2. Three parts of architecture

In an existing product architecture document, maintain three related parts,
without necessarily creating three new documents:
1. **Architectural vision.** Possible path to future scale, component/data boundary,
   expensive-to-change decisions and assumptions. Distant decisions are marked as hypotheses,
   restriction or accepted invariant; they are not an automatically approved backlog.
2. **Current architecture.** What is actually implemented at the selected stage, which
   the result provides where the limitations are, what data and tests confirm this.
3. **Development plan.** What changes are expected next, what triggers the revision,
   how the need is checked and how the transition while saving the data is possible.

The nearest stage should be worked out in detail, the further ones - to the level of significant decisions and risks.
A pre-thought-out development path does not guarantee growth without changes or mandatory
suitability of each early component. The owner allows the first prototype's code to be discarded
completely. Retention, partial replacement, or a full rewrite is chosen based on verification
results and transition cost; suitable parts are retained. There is no mandatory rewrite.
The prototype is not burdened with future reuse requirements just for the sake of
saving the code. Knowledge, tested scenarios and decisions made are saved from the experiment.
Replacing code does not itself authorize losing real user data: once such data exists, the
transition plan must separately ensure its preservation or an agreed lifecycle.

Example, not stack requirement: future image processing can be pre-allocated
as a separate operation, while maintaining a simple execution method in the MVP. During the transition to growth
measurements determine whether a queue and individual workers are needed, which ones, and how to connect them.

### 5.3. Review before scaling

Before the transition, the team checks the architectural vision with the actual load, cost,
user behavior, operational issues and changes in requirements.
The result is a versioned transition plan: what is retained, what changes, why, the expected effect,
how it will be verified, how data will be migrated, and how to roll back if necessary.

An independent review simultaneously checks the readiness of the current solution and the feasibility of the path
development. It reveals both the premature implementation of future infrastructure and solutions
that unreasonably make the next crossing expensive or unsafe.
The revision is included in the regular PLAN review of the next stage/module; don't create
duplicate approval if the same package already contains an architectural transition.
The product coordinator presents the owner with clear consequences, costs, risks and
recommendation: continue the original path, adjust it, replace a separate solution
or delay growth. Owner approves the next step plan and significant deviations;
internal details remain with the team. The old architectural vision does not replace this solution.

Don’t wait for the exact achievement of 10/100 thousand: load forecast, cost, new requirements
or measurement data may trigger the revision earlier. The stage number itself
does not warrant microservices, queue, cache, or multi-region hosting.

### 5.4. Depth of preparation and readiness criteria

Before prototyping, it is enough to define the user, hypothesis, scenario, significant restrictions,
verification method, a brief decision on the feasibility of the experiment from Gate 3.5 and permitted
demonstration conditions. Early architectural vision may
immediately take into account the large scale. Full PRD/financial model/production infrastructure plan
are not necessary preliminary work for such a limited experiment.
This does not close the corresponding gates for MVP or public release.

For each stage, explicitly select scope, depth of artifacts/reviews/checks, deadline or budget
when making an investment decision, restrictions and transition criteria. Process volume
must correspond to the scale of work; quality testing does not require repeating
full research and decisions already made for every change.
Pending requests receive a reason and return condition rather than a dummy PASS.
At the next stage, the affected gates are reopened, the existing evidence is preserved.

### 5.5. Lightweight viability assessment before Journey

Gate 3.5 answers the question: is it worth spending time and money on the next step and what
must be tested first? The result is a short note, approximately one page,
in an existing discovery document. Separate file, calculation table or finance skill
not required. This is an estimate and not proof of demand or profitability.

It is enough to indicate:

- **Market and accessible audience:** the segment's approximate order of magnitude, the share that
  could realistically be attracted, and a possible first channel. Do not substitute the size of
  the entire industry for the accessible market.
- **Competition:** several significant competitors and substitutes, including the customary way of
  solving the problem; prices, if available, and why the user might choose the product.
- **Economy:** who pays and for what, approximate price/income range, main one-time
  and recurring costs, including development, acquisition and operation; order of resources
  for the next check. Simple estimates with explicit assumptions are enough.
- **Unknowns and the next step:** what can change the conclusion the most, how small
  an experiment will test it, and which result warrants continuing or revising the decision.

For external information, indicate the source and date; distinguish between facts, estimates and unknowns.
Unavailable data should not be replaced with fictitious numbers. Do not require exact CAC/LTV, cohorts,
monthly model for 24 months, workbook or universal profit goal. For internal
or non-commercial product, evaluate benefits and allowable costs instead of revenue.

The product coordinator brings the owner a conclusion with justification and the next step:
continue, do a limited experiment, change the idea, or stop.
Permission for an experiment is limited to its purpose and resources; it does not mean approval of
the entire development effort. When data is insufficient, an experiment is acceptable instead of a
fictitious positive conclusion.
Combine this decision with approval of the same next step, without a second approval.

Boundaries of adjacent stages:

- **3 Positioning** identifies audience, alternatives and promised value. Gate 3.5
  uses these results and adds a feasibility test;
  unchanged competitor analysis is not repeated.
- **4 Journey** describes user behavior for the selected direction and takes into account
  restrictions/hypotheses from 3.5. It does not repeat market assessments or financial calculations.
- **8 Finance** clarifies the same assessment after scope/PRD: cost, monetization and sensitive
  assumptions for a particular investment decision. A detailed model is needed only when
  warranted by the scale of investment and uncertainty; an early prototype does not require it.

Findings from 3.5 feed into Scope, PRD and future plans as constraints, assumptions and issues
for checking. Changing the audience, monetization, cost or acquisition channel returns
to the affected assessment; unchanged facts do not require repeated research.
When implementing workflow, replace the old Gate 4.5 in all active entrypoints, references,
templates, and checks; move the detailed requirements of the former early assessment into the
applicable conditions of Gate 8. Do not leave two early economic gates. When updating an existing
project, accept suitable Gate 4.5 materials as evidence for Gate 3.5 and request only what is missing
or no longer current. Do not rewrite the historical baseline or old decisions.

Do not require sequential waiting where independent preparatory work
acceptable: for example, the collection of market information begins after the segment is defined,
and the final Gate 3.5 decision uses the Positioning results and precedes the detailed Journey.
In this case, the exit condition is not declared fulfilled before the required evidence/decisions.
Research must not invent interviews, metrics, or financial values. Missing data leads to an
experiment plan and explicit uncertainty.

PM, UX, finance, security and challenge are the roles of the current stage. They don't have to be permanent
user chats. Responsibility is determined by the lifecycle, the method of execution is
available tools and the user's mandate. The owner reviews local results in the task chat;
project-wide decisions and escalations go to the Product coordinator under §§6–7.

## 6. Modules, implementation and review

One main Product coordinator per product is responsible for the overall architecture, roadmap, and
dependencies between modules. One user-owned Task coordinator per large module is the owner's
primary place of work on that module. All local approvals, feedback,
planning and acceptance take place there within the delegated scope. Decisions are saved in
versioned artifacts so that they can be restored without a complete rewrite.

The task coordinator checks the current implementation, binding sources and the actual manifest,
describes what/why, observable behavior, failure/recovery, non-goals and acceptance criteria
for the selected stage; Links ongoing implementation to the architectural vision and development plan.
PLAN reviewer independently verifies the complete plan in this scope, including architecture transition
when scaling. Task coordinator presents the version with PLAN_PASS to the owner in chat
task. There is no need to re-approve the same version with the Product coordinator.

After permission: Work Item → Issue, if needed → isolated branch/worktree →
Implementation subagent → independent Change Review subagent → one PR → manual merge.
PLAN and FINAL also run separate read-only subagents under the Task coordinator.
Each subagent receives a limited task and a separate context. Reviewer receives
requirements and a verifiable result without a history of the performer’s reasoning. General file
the system does not provide change isolation: one writer per workspace, review after
ready candidate; parallel writes are only allowed in isolated workspaces
for independent tasks with stable contracts.
Each handoff includes role, parent/report_to, approved scope/plan identity, source links,
type of executor and its native ID (task ID is not replaced by agent ID), base/head where applicable,
checks, limitations, process version, stage of development,
version of the architectural decision and next action.
The presence of a parent Issue is not required to start discovering a new product.

Previously accepted Work Items are not recreated. Their immutable evidence is included in manifest,
and compatibility is checked by affected regressions and FINAL.
Within a module you can parallelize independent Work Items; shared contracts/schema/auth/files
and dependencies require coordinated sequencing. One implementer owns each branch.

Change Review checks the full diff against binding requirements of the current stage, including
excessive complexity and adherence to accepted architectural boundaries. Future hypothesis
scaling does not turn into finding “implement now” without an actual requirement.
Findings require specific violation, evidence and observable correction.
Before merge, corrections remain in the same Work Item and branch with its implementation/review
roles; a new commit invalidates PASS. If the subagent has ended or is lost, a new session receives
the saved package without loss of evidence; its identity is recorded explicitly.
After two unsuccessful fixes of one finding or technical dead end - independent
second opinion. This is not a reason to automatically involve the owner in a technical discussion.

After merging all planned/corrective PRs, a separate FINAL subagent performs the final phase
Whole-Task Review with assigned model. Checks the result against the full immutable current-main SHA.
After FINAL, the coordinator re-compares main; drift requires updated FINAL.
Post-merge defect → new narrow corrective Work Item with Implementation/Review/PR → repeat FINAL.
Closing the parent Task is allowed only if this condition is met; next module
receives a separate reviewed plan approval.
Updating navigation is included in the explicit reviewed scope. A separate status-only Work Item is needed,
if the update is otherwise outside the scope of the current task; not required for every module.

## 7. Owner involvement and permissions

The owner works with the Task coordinator directly: module plan, local requirements/UX,
Feedback, corrections and acceptance within the framework of the approved architecture remain in the task chat.
The main Product coordinator handles the overall problem/success, project scope,
general architectural contracts, dependencies/order of large tasks, significant consequences
for cost, risk, schedule, and release. Local technical complexity alone does not require
escalation. Substantive product decisions and acceptance of residual risk remain with the owner;
the Product coordinator organizes the decision and determines further work
within the limits of the powers already granted.
Previously authorized decisions are not requested again when the version and scope are unchanged.

The decision is presented as a clear result, why it is needed, consequences and choice.
Conventional internal engineering is handled by implementers and reviewers within the accepted architecture.
They may need an internal implementation plan for their work; it does not mean additional
mandatory owner approval or a large technical document for each change.

Decision package: identifier/version or content hash, reviewer verdict, options if applicable,
recommendation, material risks, and scope. The owner's decision references the same package.
Reply "yes" without a one-to-one version match does not allow an arbitrary new scope.
The comment hash records the content, but is not the owner's electronic signature.

An owner-approved plan authorizes routine coordination, Issue/PR operations, and corrections within
its scope when current platform permissions are sufficient. GitHub login certifies
account access, but does not replace the mandate for action.

The platform may not accept retelling of consent. In case of refusal: write down the action, purpose,
a brief reason; continue to work independently; inform the owner of a specific block in chat
execution, escalate beyond local mandate. Do not repeat the request every heartbeat,
do not change transport/credentials/executor
to bypass the failure. If direct platform confirmation is required at the execution location,
explain this exception to the owner at the place of performance; Don't promise to eliminate it with one skill.
Manual merge remains an explicit separate action by the owner.

### 7.1. Events between coordinators

The Task coordinator sends only changes to the main states to the Product coordinator:
`ACTIVE`, `ESCALATION_REQUIRED`, `READY_FOR_INTEGRATION`, `DONE`, `CANCELLED`.
The message contains a task, an event, a brief reason/result and a link to evidence; for
escalation, it includes the required decision. Repeated unchanged state, subagent logs, the full
manifest and all approvals are not sent upstairs. Product details reads as needed.
These are signals of coordination, not a second base Issue/PR/CI: facts are checked in GitHub/native state.
`READY_FOR_INTEGRATION` requires an up-to-date Change Review and a ready PR if allowed.
`DONE` for the delivery module means manual merge of all changes and FINAL_PASS on the unchanged one
current main without mandatory open patches; merge alone is not enough to close.
For a non-code task, `DONE` is determined by its own acceptance criteria.

Escalation contains the problem and evidence, the violated boundary, the affected tasks, options
and a recommendation, a solution required, and work that can proceed. Suspended
dependent part only; independent authorized work continues.

### 7.2. Architecture re-planning

Product coordinator solves a small issue within the mandate or if necessary
creates a permitted separate user architectural task. Its coordinator
analyzes options, risks and new decomposition with subagents; independent reviewer
checks the result. Package includes new architecture version, list/dependency changes
tasks, preserved work, and resumption conditions. The owner's substantive decision is agreed once
in that task or the main chat and linked to the package version.
The product coordinator records the decision made, updates project-wide artifacts, and
communicates only the new boundaries and the next action to the affected Task coordinator.
Those revise the affected plans/review and resume work once the conditions are met.
The new architecture does not automatically permit a new scope of implementation.

## 8. Native tools, access and recovery

Delivery v0.1 requires accessible tools for creating/reading tasks, native messages,
compact waiting and sustainable resumption of the coordinator. Runtime reference describes
their meaning and actual compliance with the tools of the current environment, rather than the native RPC API.

Creating user-owned coordinator/architecture tasks requires the user's mandate and
compliance with environmental constraints. Implementation/PLAN/Change Review/FINAL - internal
subagents according to the agreed topology, not additional user chats.
The unavailability of a capability is reported accurately; you cannot promise constant background work or
lack of platform confirmations only due to skill. Migration of old held tasks
preserves WIP/evidence and requires a current reviewed plan; it is not used to bypass a denial.
Discovery can continue even if future delivery coordination is unavailable.

Task ID and agent ID are of different types: the internal agent ID is not passed to the user API
tasks and vice versa. Real parent/report_to IDs are used before descendant creation. For queued creation
The usable thread ID is first resolved, then the self ID is passed. Don't create a duplicate
due to the absence of a task in the first list. Recovery uses the existing Issue/PR manifest,
approved decisions, Git evidence and native task state; the base is not built on top of the Codex base.

One heartbeat per waiting coordinator, start interval 5 minutes, silence when
unchanged condition. Continue waiting only as long as there is a useful next transition.
When finished, stop/remove according to the current requirements of the tool/environment.
The notification method and format are also determined by the current environment. Don't promise a job
desktop turned off; after resuming, first check the facts, do not perform all the steps again.

GitHub: gh with explicit host/repo; before the first service action bounded authenticated read-only
check. The path is discovered in the environment, without token extraction. Git is responsible for fetch/local commits
and allowed push. For API mutate, use the exact body via file/input, not shell interpolation.
Agent GitHub UI/browser/CUA, gh browse/--web and alternative transport/credentials fallback
excluded. The owner can view and merge through the GitHub UI.

## 9. Models and skills

The current profile uses the owner's 2026-10-05 model update. The earlier approved
Recipes matrix established the role boundaries; the model IDs below are current
assignments, not the IDs used by the historical project:

| Work | Model/reasoning |
|---|---|
| Product/Task coordination, decomposition, PLAN review | gpt-6-sol/high |
| Regular implementation and clear bugfix | gpt-6-sol/medium |
| Small unambiguous change with low risk, trial mode | gpt-6-luna/medium |
| Complex debugging | gpt-6-sol/high; escalation gpt-6.1-sol/high |
| Change Review, including requirements/UX | gpt-6-sol/high |
| Essential architecture, security review, FINAL, second opinion | gpt-6.1-sol/high |

For early research/PM/finance/UX roles, gpt-6-sol/high is offered in the starting profile;
this is a v0.1 role offering and was not part of the historical Recipes selection.
Matrix - product configuration. Runtime availability check; no model
does not allow silent substitution. When create/follow-up, pass native model/reasoning fields
and distinguish the assigned model from the independently validated factual one.

Third-party skills are called by the capability of the current gate. Dependencies reference for each
contains the purpose when needed, the found name/version and the validity of the fallback.
Do not install the entire directory or plugins silently and do not consider the readme-list as proof of availability.
The presence of a named specialist skill does not replace checking its results.

If the PM skill is missing, report the missing specialization and follow the procedure
within the framework of the original fallback policy; preserve the uncertainty of the results.
If grill-me is missing, an independent PRD challenge under the explicit workflow category is allowed.
Financial replacement follows financial-model reference with changes §5.5: lightweight Gate 3.5,
proportional investment clarification in Gate 8, without returning the heavy early requirements of the baseline.
If the security/finance check cannot be performed efficiently using available means,
the corresponding gate remains open; generic response does not become PASS.

Don't hardwire made-up dependencies into openai.yaml as a supported installation mechanism.
Specialist instructions that require unnecessary approvals or conflict with scope,
are checked against the user's explicit decisions and operating constraints.

## 10. Checking the workflow itself

Two levels:

- Mechanical checks: skill metadata/relative references, required readiness fields,
correct version identity, absence of Recipes-paths/IDs in active templates,
  semantic incompatibilities of state fields (for example PASS for another head).
- Behavioral assessment: an individual agent receives a user request and minimal fixtures,
  without the expected response; reviewer checks real actions on EVALUATION.md.

Don't give docs lint as semantic PASS. Don't build a runtime enforcement engine for the sake of
offline fixture checks. If the script does not provide repeatable benefit, leave the procedure.
Metrics: manual transfers, duplicate owner prompts, unsolicited scope expansions,
incorrect transitions, lost handoffs, phase costs when data is available.
Don't advertise time/token savings without measurements.

## 11. Implementation and release v0.1

This is a delivery order, not permission to immediately carry out the following:

1. Move the package to a separate project provided by the owner. Save original seven files first
   baseline commit with origins, without rewriting them or making up historical commits.
2. Agree on the general project specification in the main coordination chat of the workflow project.
3. Create a detailed bounded delivery plan: updating the initial references/entry points;
   runtime/roles/templates; checks/fixtures; pilot and installation. Each delivery item
   receives an independent review according to the scheme adopted for the new project.
4. Run offline evaluation in isolated fixtures; correct real behavior errors.
5. Go through a small synthetic product from idea to release rehearsal; external publications,
   messages to people and paid operations are performed only in an explicitly permitted pilot.
6. Check re-installation, drift detection, resume and return to the previous version.
7. Release v0.1 with actual supported feature matrix and known limitations.

## 12. Acceptance criteria

- The original product-development-cycle is recognizably developed and not replaced by a competing skill.
- All corrections A01–A24 have an implementation or explicit justification for the exception.
- Between Positioning and Journey there is one lightweight assessment at Gate 3.5; later Finance refines it
  according to the scale of investment. There is no required detailed model prior to prototype or duplicate 4.5.
- Architectural vision, current implementation and development plan are distinguishable; five steps
  have their own scope/evidence and do not turn into one early production delivery.
- Before scaling, facts may change the original architectural path;
  The readiness criterion includes a measurable load profile, not just the number of accounts.
- Active templates do not contain Recipes-specific binding requirements, personal paths and foreign IDs.
- In a new project, you can define the first gate and continue from the existing state.
- Decisions are made at the appropriate level without repeated approval; routine relay
  does not require a person, upward events are compact, project-wide changes are escalated.
- PLAN, Change Review and FINAL are distinguishable; the wrong version of evidence does not give PASS.
- No automatic merge, bypass of a denial, or unrequested model change.
- Inapplicable gate is separated from unverified; release is not announced by one green CI.
- All critical scenario cases pass; the rest have an obvious result/limitation,
  without a blanket waiver of security or evidence validity requirements.
- Installation and update are reproducible, there is verifiable version identity and rollback.
- The pilot was assessed independently; release rehearsal is not named production release.

## 13. Remaining decisions

For the transfer, the name and public repository have already been selected by the owner:
`WorkKroG/product-development-harness`; the local project has been created.
To implement `FWP-PLAN-v1`, a Markdown profile has been approved, the minimum composition of the working
slice, include status/navigation updates in the nearest reviewed scope, Sol/high for
early PM/finance/UX roles and synthetic pilot QuietFollow. FWP allows local
fixtures, isolated branches/worktrees and necessary Codex tasks after PLAN review;
GitHub mutations, push, global installation, paid actions and production release
are not included in this mandate.

For publication, decisions remain regarding the license/origin of transferred materials and
exact public scope. For MVP there remains clean installation/update/rollback, complete
E01–E41 and separately permitted live GitHub rehearsal.

These decisions do not interfere with ongoing audits. They do not mean a re-affirmation already
roles agreed in conversation, the Codex-only scope, or existing Recipes product decisions.
