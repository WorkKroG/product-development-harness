# Product Development Workflow — Module 4 C03 Bounded Scanner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development`
> to implement this plan task-by-task under the Task topology in `AGENTS.md`. PLAN,
> Implementation, Change Review, adversarial review, and FINAL are distinct bounded internal
> agent sessions. Do not begin Implementation until the owner accepts this exact plan identity.

**Identifier:** `MODULE4-C03-REPLAN-v1`. PLAN identity is the SHA-256 of this file plus the exact
base below. Any content or base change invalidates `PLAN_PASS`.

**Goal:** replace C03 partial-match extraction with a deterministic bounded scanner that consumes
whole supported inline link and image constructs, so excluded images cannot hide adjacent links and
every supported link destination reaches the existing classification and filesystem validation.

**Architecture:** a small standard-library state scanner walks each Markdown line from left to
right and emits typed whole constructs: valid link, valid image, or recognized-invalid construct.
Valid images are consumed without sending their destinations to link validation; valid links send
exactly one destination to the existing C03 classifier; recognized malformed constructs fail C03.
Classification, containment, symlink checks, output schema, and evidence remain separate and
unchanged.

**Tech Stack:** Python 3 standard library (`dataclasses`, `pathlib`, `re`, `typing.Literal`, `urllib.parse`,
`unittest`, `subprocess`, `tempfile`, `shutil`), existing structural-checker interfaces and Git.

**Spec:** `SPEC.md` §§6–10 and §12; `AUDIT.md` A07, A11, A13, A14, A18–A21;
`EVALUATION.md` E12, E13, E17–E22, E26–E30, E38–E41; parent plan
`docs/superpowers/plans/2026-09-07-module-4-deterministic-structural-checker.md`, especially C03;
accepted Product decision to preserve the existing C03 requirement and perform a bounded redesign
after four post-merge Important extraction/classification findings.

## Global Constraints

- Exact base: `939980ded8fb2be14fb8e5a32c3302f5ad56fd33`, freshly fetched from
  `origin/main` on 2026-09-09; `FETCH_HEAD` and `origin/main` matched.
- Current product maturity remains `working-prototype`; this is structural evidence only.
- Preserve the parent C03 semantics: inspect destinations of supported inline Markdown links;
  exempt only `http`, `https`, `mailto`, and fragment-only destinations; validate scheme-free local
  paths inside the active skill as existing bounded regular files.
- Preserve image exclusion: image destinations are not link targets, but a complete supported image
  must be consumed so its label, destination, and title cannot hide a real adjacent link.
- Use only the Python standard library. No parser dependency, new supported scheme, public API,
  active-skill semantics, CI design, installation, release, pilot, or Module 5 work.
- Do not modify C01 or any other C-check behavior.
- Allowed tracked paths for the future candidate are exactly:
  `docs/superpowers/plans/2026-09-09-module-4-c03-bounded-scanner.md`,
  `scripts/check_workflow.py`, and `tests/test_check_workflow.py`.
- Preserve all prior commits, PRs, reviews, and ignored local evidence. Do not replay completed work.
- Planning/PLAN review: `gpt-5.6-sol/high`; Implementation: `gpt-5.6-sol/medium`; Change Review:
  `gpt-5.6-sol/high`; pre-publication adversarial review: `gpt-6-astra/high`; post-merge FINAL:
  `gpt-6-astra/high`. Requested assignment, accepted native assignment, and independently verified
  runtime fact remain separate fields.
- Required limitation: `Structural checks do not prove behavioral correctness.`

---

## Why the previous fixes did not close C03

The defect is not a proven model or context-window limitation. The concrete cause is architectural:
the checker searched for partial link-shaped substrings instead of tokenizing whole constructs.
An image opener was excluded by a negative lookbehind, but the scanner then continued inside that
image's quoted title. Link-like title text became a fabricated HTTPS destination, absorbed the real
adjacent missing link, and received the external-scheme exemption.

The earlier tests and reviews mostly varied one dimension at a time:

- destination-only matrices began after extraction and could not prove that a link was found;
- isolated image tests proved exclusion but not full image consumption;
- adjacent-link tests lacked image titles containing link-like text;
- positive PASS tests could succeed because a construct was silently omitted;
- reviews checked the submitted matrices, but the cross-product of wrapper, context, and destination
  was not independently attacked before publication.

This plan corrects the abstraction boundary and review sequence rather than adding another regex
exception.

## Supported bounded grammar

The scanner processes one physical line at a time. It recognizes only these whole constructs:

```text
construct     := link | image
link          := "[" label "](" payload ")"
image         := "![" label "](" payload ")"
label         := zero or more label-character
label-character := any code point except "[", "]", "\\", control, CR, and LF
payload       := horizontal-space* destination (horizontal-space+ quoted-title)? horizontal-space*
destination   := plain-destination | angle-destination
plain-destination := zero or more characters except space, tab, "(", ")", "\\", control, CR, and LF
angle-destination := "<" zero or more characters except ">", "\\", control, CR, and LF ">"
quoted-title  := single-quoted-title | double-quoted-title
single-quoted-title := "'" zero or more characters except "'", "\\", control, CR, and LF "'"
double-quoted-title := '"' zero or more characters except '"', "\\", control, CR, and LF '"'
```

Clarifications:

- `horizontal-space` means exactly ASCII space U+0020 or tab U+0009. `control` means U+0000
  through U+001F or U+007F; horizontal-space is allowed only where the productions name it.
- `_read_path_text` supplies newline-normalized text. `_scan_inline_constructs` splits only on
  `"\n"`; each element is scanned independently and the separator is never part of a construct.
- Empty and nonempty labels are supported.
- An empty link destination is recognized and then rejected by link classification. An empty image
  destination is consumed and ignored because image targets are outside C03 link validation.
- `)` and link-like text are allowed inside angle destinations and quoted titles.
- Spaces are allowed only inside angle destinations or quoted titles.
- Single and double quoted titles are supported; parenthesized titles are not.
- Adjacent constructs are supported with no separator.
- A complete image produces no link candidate, but its full span advances the scanner cursor.
- The emitted destination is the exact plain-destination substring or exact content between `<` and
  `>`; the scanner removes only payload-leading spacing and angle delimiters. It does not trim,
  unescape, decode, case-fold, or otherwise normalize destination text.
- A recognized opener with `](` that cannot complete the grammar emits one invalid construct and
  makes C03 fail closed. It must not manufacture an exempt destination.

Unsupported-form disposition is explicit:

- An opener is escaped when immediately preceded by an odd-length run of backslashes. `\[` and
  `\![` are ordinary text, emit no token, and are advanced past as whole opener sequences; a later
  independent unescaped opener is still scanned. Even-length runs do not escape the opener.
- For an unescaped `[` or `![`, inspect the next unescaped opener and the next `](` on the same
  physical line. It is a recognized candidate only if its `](` occurs first. If another unescaped
  opener occurs first, the current opener is ordinary text and scanning resumes exactly at the later
  opener. This prevents a literal `[` from claiming a following independent image or link.
- The first qualifying `](` is the candidate payload boundary. If the intervening label or following
  payload violates the grammar—including a prohibited bracket, backslash, control, balanced bare
  destination, parenthesized title, malformed quote, or malformed angle destination—it emits one
  `invalid` token.
- Invalid recovery never rescans the candidate interior. Starting at the payload opening `(`, find
  the first following `)`: resume exactly one code point after it. If no `)` remains, resume at
  end-of-line. Thus `[bad](x title)[ok](references/lifecycle.md)` emits `invalid` and then the valid
  adjacent link, while `[bad](x "unterminated [maybe](references/lifecycle.md)` emits only `invalid`:
  its first following `)` is consumed as the recovery boundary, so the ambiguous interior is never
  rescanned. Both inputs make C03 fail.
- A bracket without a same-line `](` signature is ordinary text outside this inline-link contract.
  Reference-style links, multiline forms, HTML/autolinks, and literal brackets therefore do not
  become supported candidates or exemptions. Code spans/fences are not interpreted: link-shaped
  text inside them is scanned by the same rules. Extending C03 to other Markdown forms requires a
  separate contract decision and PLAN review.

Explicit non-goals are reference-style links, nested labels, escaped labels or delimiters, escaped
quoted-title content, balanced parentheses in a plain destination, multiline links,
HTML/autolinks, code-span or fence semantics, URI decoding, remote reachability, new schemes, and
full CommonMark compliance. These forms are not silently reclassified as supported. If active
workflow content needs one, change the contract and repeat PLAN review rather than extending this
scanner opportunistically.

## Interfaces and state model

Add one private token type and two private scanner helpers in `scripts/check_workflow.py`:

```python
@dataclass(frozen=True)
class InlineConstruct:
    kind: Literal["link", "image", "invalid"]
    destination: str | None


def _scan_inline_constructs(content: str) -> tuple[InlineConstruct, ...]:
    """Return whole bounded constructs in source order."""


def _scan_inline_construct(line: str, start: int) -> tuple[InlineConstruct | None, int]:
    """Parse at start; always return a next index greater than start."""
```

Scanner state is local to a line. At each position:

1. If the text starts with `![`, select an image opener and never reconsider its `[` as a link
   opener. Otherwise, if it starts with `[`, select a link opener. Apply the odd-backslash escape
   rule before selection.
2. If neither unescaped opener begins at the position, advance one code point.
3. From a selected opener, find the index of the next unescaped opener and the next `](`. If the
   later opener exists and the `](` is absent or not earlier, emit no token and resume at that later
   opener. If neither qualifying boundary exists, emit no token and advance past the current opener.
   Otherwise use the `](` as the payload boundary and validate the intervening label. A prohibited
   label character takes the invalid-recovery transition.
4. Parse the complete payload using the exact character classes and delimiter-aware angle/title
   states above. First consume all payload-leading horizontal-space; those characters never serve as
   the title separator. Then choose angle destination when the next character is `<`, otherwise scan
   a plain destination greedily. Only horizontal-space encountered after that destination may begin
   a quoted title. Therefore `[x]( 'title')` has plain destination `'title'`, while `[x]( )` has an
   empty destination. Preserve extracted destination text except for the explicitly removed syntax.
5. On a valid image, emit `kind="image"`, consume through its closing `)`, and continue after it.
6. On a valid link, emit `kind="link"` with the exact extracted destination, consume through its
   closing `)`, and continue after it.
7. On a recognized but malformed construct, emit `kind="invalid"`; use the first-`)`/end-of-line
   recovery rule above. Never resume inside the consumed invalid span and never emit a destination
   synthesized from malformed text.

`check_c03(root)` consumes the tokens as follows:

```python
for construct in _scan_inline_constructs(markdown):
    if construct.kind == "image":
        continue
    if construct.kind == "invalid" or not construct.destination:
        failures.append(relative_source)
        continue
    destination = construct.destination
    # Existing urlsplit classification and bounded filesystem validation continue unchanged.
```

The scanner does not read the filesystem. The classifier does not inspect labels, titles, or image
targets. This separation is the load-bearing design boundary.

## Required invariants

1. Every supported non-image link emits exactly one `link` token, independent of label length.
2. Every complete supported image emits exactly one `image` token and zero link destinations.
3. A supported image consumes its whole title and resumes immediately after its closing `)`.
4. An adjacent supported link remains observable even when the image title contains link-like text.
5. Empty or invalid link destinations become failures; they never disappear during extraction.
6. Invalid syntax never becomes `http`, `https`, `mailto`, or fragment-only through normalization.
7. A successful token advances past its whole closing delimiter; its title is never rescanned.
8. A malformed recognized construct terminates deterministically and cannot cause an infinite loop.
   A later supported construct remains observable whenever the malformed construct has its own
   first `)` recovery boundary; boundary-ambiguous remainder is consumed but C03 already fails.
9. Existing scheme, authority, pathless, absolute, escape, missing, directory, containment, and
   symlink decisions remain unchanged.
10. C03 evidence remains sorted, deduplicated, repository-relative, and destination-redacted.
11. A literal or escaped opener cannot claim a later independent supported construct.

## Combination matrix

Each negative case uses a fresh copied repository. Pairwise rows cross the three dimensions that
previous reviews treated separately:

| ID | Wrapper | Context | Destination | Expected |
|---|---|---|---|---|
| M01 | named link | isolated | existing local | PASS and one link token |
| M02 | empty-label link | isolated | existing then missing control | PASS then FAIL; both extracted |
| M03 | named/empty link | isolated | empty, whitespace, angle-empty | FAIL |
| M04 | named/empty link | isolated | `//host`, `//host/path`, query-only | FAIL |
| M05 | named/empty link | isolated | `ftp`, `file`, arbitrary scheme to existing path | FAIL |
| M06 | named/empty link | isolated | HTTP/HTTPS/mailto, `#`, fragment with `?` | PASS and extracted |
| M07 | link | plain/angle + single/double title | existing and missing local | target-dependent PASS/FAIL |
| M08 | link | angle/title contains `)` or link-like text | existing and missing local | target-dependent PASS/FAIL |
| M09 | image | isolated, empty/nonempty label, plain/angle/title | any target | image token only; C03 PASS |
| M10 | image | quoted title contains fake allowed/invalid link text | any target | image token only; C03 PASS |
| M11 | image + link | adjacent, title contains fake link text | missing/unsupported adjacent link | C03 FAIL on real link |
| M12 | image + link | adjacent | valid local/exempt adjacent link | C03 PASS; one image + one link |
| M13 | literal/escaped opener + image + link | exact literal `[ ![image](...)[](...)`; odd `\[x](...)`, `\![x](...)`; even `\\[x](...)` | valid/missing | literal/odd-escaped opener emits nothing; even/unescaped and independent constructs retained |
| M14 | two or three links | adjacent/repeated | last missing | FAIL; every link token present |
| M15 | malformed recognized link/image | exact cases: `[x](p title)`, `[x](p 'mismatch\")`, `[x](<p)`, `[x](p\q)`, Python `"[x](p\x01)"` with runtime U+0001 | any | one invalid token; first-`)`/EOL recovery; FAIL |
| M16 | recoverable malformed link/image + valid adjacent link | exact cases: `[bad](x title)[ok](references/lifecycle.md)` and `![bad](x title)[](<references/lifecycle.md>)` | existing local | invalid then link token; deterministic FAIL |
| M17 | valid construct at line end and next-line construct | separate lines | existing/missing | no cross-line capture |
| M18 | local link | bounded `..`, absolute, escape, directory, leaf/ancestor/dangling symlink | filesystem contract unchanged |

All historical reproducers remain explicit regression inputs: network paths; named empty/whitespace
destinations; `#`; unsupported schemes; angle-plus-title; empty labels; title-rescanning; image-title
swallowing of adjacent missing and unsupported-scheme links.

## File map

- Include `docs/superpowers/plans/2026-09-09-module-4-c03-bounded-scanner.md` — this accepted,
  identity-bound correction plan.
- Modify `scripts/check_workflow.py` — replace `_extract_inline_destinations` with the typed bounded
  scanner and route C03 link tokens into the unchanged classifier.
- Modify `tests/test_check_workflow.py` — scanner token tests, end-to-end matrix, historical
  regressions, CLI determinism/redaction, and mutation-sensitive positive controls.
- Do not create tracked fixtures; temporary files and symlinks stay inside per-test directories.

## One Implementation Work Item

### Task 1: Replace partial matching with whole-construct scanning

**Files:**

- Include: `docs/superpowers/plans/2026-09-09-module-4-c03-bounded-scanner.md`
- Modify: `scripts/check_workflow.py` in the private C03 extraction helpers and `check_c03`
- Test: `tests/test_check_workflow.py` in dedicated scanner, direct C03, and CLI test groups

**Interfaces:**

- Consumes: active-skill Markdown text already read through `_read_path_text`; current C03
  `urlsplit` classifier; `_has_symlink_component`; bounded regular-file and containment helpers.
- Produces: `InlineConstruct`, `_scan_inline_construct`, `_scan_inline_constructs`; unchanged public
  CLI and `Check("C03", ...)` result contract.

- [ ] **Step 1: carry the accepted plan unchanged onto the execution branch**

  Run:

  ```sh
  git fetch origin main
  git switch -c codex/module-4-c03-bounded-scanner 939980ded8fb2be14fb8e5a32c3302f5ad56fd33
  git rev-parse HEAD
  shasum -a 256 docs/superpowers/plans/2026-09-09-module-4-c03-bounded-scanner.md
  git status --short
  ```

  Expected: exact base above; accepted plan hash; status shows exactly the untracked accepted plan
  path carried from the planning worktree and no other change. A different base, plan hash, or path
  set pauses execution for identity review. The plan remains byte-identical until staged with the
  implementation candidate.

- [ ] **Step 2: add RED token-sequence tests for the supported grammar**

  Add `WorkflowInlineConstructScannerTest` with literal expected tuples. Representative assertions:

  ```python
  self.assertEqual(
      (
          self.checker.InlineConstruct("image", "https://example.invalid/image.png"),
          self.checker.InlineConstruct("link", "references/missing.md"),
      ),
      self.checker._scan_inline_constructs(
          '![image](https://example.invalid/image.png "fake [inner](<https://example.invalid/path")'
          '[](<references/missing.md>)'
      ),
  )
  ```

  Add literal token expectations for every extraction-sensitive row M01–M17. In particular, assert
  the exact emitted destinations for M02–M06: empty-label existing/missing, empty/whitespace/angle-
  empty, `//host`, `//host/path`, query-only, `ftp`, `file`, arbitrary scheme, HTTP/HTTPS/mailto,
  `#`, and fragment-with-query. Also cover empty image destination, single/double titles, `)` and
  link-like title text, adjacent/repeated constructs, a literal bracket before an image, and line
  boundaries. Assert the odd/even escaped-opener cases and the leading-space precedence cases
  `[x]( 'title')` → destination `'title'` and `[x]( )` → empty destination. For M15/M16, use the
  literal malformed and recovery strings in the matrix and assert exact ordered token tuples.
  Expected values are hand-written and do not reuse scanner logic.

- [ ] **Step 3: run scanner tests and verify RED**

  Run:

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowInlineConstructScannerTest -v
  ```

  Expected: FAIL because `InlineConstruct` and `_scan_inline_constructs` do not yet implement the
  typed whole-construct contract. Record the missing-interface failures as the intended RED result;
  the real old-extractor false PASS is demonstrated independently by the direct C03 RED in Step 6.

- [ ] **Step 4: add RED end-to-end direct C03 matrix tests**

  Add fresh-root cases for M01–M18. Positives use paired mutations so PASS cannot mean omission:

  ```python
  valid = "[](<references/lifecycle.md> 'title ) [fake](missing)')"
  invalid = "[](<references/missing.md> 'title ) [fake](missing)')"
  self.assert_check(run_case(valid), "C03", "PASS")
  self.assert_check(run_case(invalid), "C03", "FAIL")
  ```

  Direct C03 tests must not call the missing scanner interface before implementation. Keep them in
  separate test methods from Step 2 while sharing only literal input constants. Cover M01–M18,
  including the allowed-scheme and fragment-only PASS cases, paired valid/missing destinations,
  valid images, image-plus-link cases, escaped/literal opener counterexamples, malformed recovery,
  and the unchanged M18 filesystem branches. After GREEN, the separate scanner tests prove that
  each PASS/FAIL case reached C03 with the expected token rather than succeeding by omission.

- [ ] **Step 5: add RED subprocess CLI regressions**

  Add independent cases for:

  ```text
  empty-label missing link
  image with fake HTTPS title text + adjacent missing link
  image with complete fake link title text + adjacent unsupported-scheme link
  valid image + adjacent valid empty-label angle/title link
  malformed recognized image + adjacent valid link
  ```

  Every failing case asserts exit `1`, empty stderr, twelve ordered checks, only C03 failed,
  repository-relative source evidence, no root or destination disclosure, and the mandatory C12
  limitation. Run one adversarial failure twice and require byte-identical stdout.

- [ ] **Step 6: run direct and CLI selections and verify RED**

  Run the old-C03 behavior selection first, independently of the missing scanner interface:

  ```sh
  python3 -B -m unittest \
    tests.test_check_workflow.WorkflowStructuralChecksTest \
    tests.test_check_workflow.WorkflowCheckerCliTest -v
  ```

  Expected: the current image-title/adjacent direct and CLI regressions fail because old C03 falsely
  reports PASS; other unrelated C-check tests retain their prior results. Then run:

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowInlineConstructScannerTest -v
  ```

  Expected: the scanner contract tests independently fail because the new interface is absent. Keep
  both RED outputs so the real behavior regression is not masked by an earlier `AttributeError`.

- [ ] **Step 7: implement the typed sequential scanner and integrate C03**

  Replace partial regex extraction with the interfaces and state transitions defined above. Keep the
  classifier block after token selection byte-for-byte equivalent unless a mechanical variable rename
  is required. A valid image consumes the same bounded payload grammar as a link but emits no link
  destination. An invalid recognized construct emits `InlineConstruct("invalid", None)`.

- [ ] **Step 8: run focused tests and verify GREEN**

  Run:

  ```sh
  python3 -B -m unittest \
    tests.test_check_workflow.WorkflowInlineConstructScannerTest \
    tests.test_check_workflow.WorkflowStructuralChecksTest \
    tests.test_check_workflow.WorkflowCheckerCliTest -v
  ```

  Expected: PASS. Inspect named outputs so no case is skipped and no subtest masks another.

- [ ] **Step 9: perform mutation checks on load-bearing branches**

  Temporarily test each mutation separately, then restore the candidate code:

  ```text
  treat image as link
  stop image parsing before its quoted title
  resume search at opener end instead of whole-construct end
  require a nonempty label
  turn invalid construct into no token
  resume an invalid construct inside its consumed span or past a recoverable adjacent link
  remove unsupported-scheme guard
  remove symlink-component guard
  ```

  At least one named test must fail for every mutation. Record test names and outcomes in ignored
  Implementation evidence; do not commit mutation code.

- [ ] **Step 10: run full verification**

  Run:

  ```sh
  python3 -B -m unittest discover -s tests -v
  python3 scripts/check_workflow.py \
    --root . \
    --review-state tests/fixtures/review-state/valid-final.json \
    --json
  shasum -a 256 -c BASELINE.sha256
  shasum -a 256 docs/superpowers/plans/2026-09-09-module-4-c03-bounded-scanner.md
  git add \
    docs/superpowers/plans/2026-09-09-module-4-c03-bounded-scanner.md \
    scripts/check_workflow.py \
    tests/test_check_workflow.py
  git diff --cached --check
  git diff --cached --name-only
  git status --short
  ```

  Expected: full suite PASS; checker C01–C12 PASS; baseline 7/7; accepted plan hash; no staged
  whitespace errors; staged paths exactly the plan, checker, and tests; status has those three staged
  paths and no unstaged or untracked changes. Record the structural revision and the exact
  limitation. Do not infer absence of all bugs from the number of passing tests.

- [ ] **Step 11: commit and verify the exact local candidate**

  Commit the already verified index, then verify the immutable base-to-head candidate. Run:

  ```sh
  git commit -m "fix: scan complete C03 inline constructs"
  git rev-parse HEAD
  git diff --check 939980ded8fb2be14fb8e5a32c3302f5ad56fd33..HEAD
  git diff --name-only 939980ded8fb2be14fb8e5a32c3302f5ad56fd33..HEAD
  shasum -a 256 docs/superpowers/plans/2026-09-09-module-4-c03-bounded-scanner.md
  git status --short
  ```

  Expected: one clean local candidate identity; no whitespace errors; changed paths exactly the
  three allowed paths; accepted plan hash unchanged; clean status. No push or PR follows without
  separate permission.

## Independent pre-publication gates

### Task 2: Change Review and adversarial review

**Files:**

- Inspect: exact base-to-head diff and all three allowed paths
- Evidence only: ignored Task ledger and immutable review packages

**Interfaces:**

- Consumes: accepted plan ID/hash/base, exact candidate head, full diff, test output, mutation record,
  supported grammar and combination matrix.
- Produces: two independent exact-head verdicts: Change Review and bounded adversarial review.

- [ ] **Step 1: run independent Change Review**

  A fresh `gpt-5.6-sol/high` read-only reviewer receives the plan/hash, exact base/head, full frozen
  diff, source files, test matrix, mutation results, and binding sources without Implementation
  conversation. It reviews spec compliance, scanner termination/consumption, classifier preservation,
  deterministic evidence, test independence, and non-goal containment.

  Verdict is `PASS` only with no unresolved Critical/Important findings. Any new head invalidates it.

- [ ] **Step 2: run independent bounded adversarial review**

  After Change Review PASS, a separate `gpt-6-astra/high` read-only session receives the same exact
  identities and supported grammar but not the author's conversation. It must generate and execute a
  fresh wrapper × context × destination matrix, including all historical reproducers and positive
  counterexamples against false FAIL. It must observe emitted tokens as well as C03/CLI results, so
  PASS-by-omission cannot satisfy the review.

  Verdict is `ADVERSARIAL_PASS` only when every supported construct is consumed exactly once, images
  cannot hide adjacent links, unsupported recognized syntax fails closed, classification/filesystem
  behavior is preserved, and no Critical/Important finding remains. Any new head invalidates both
  pre-publication verdicts; repeat both reviews after corrections.

- [ ] **Step 3: repeat coordinator verification on the exact reviewed head**

  Repeat the full suite, checker, baseline, plan hash, diff-path/whitespace checks, worktree status,
  and a fresh `origin/main` fetch. Preserve exact outputs and limitations in ignored evidence.

- [ ] **Step 4: stop for publication authorization**

  Report the local candidate with exact base/head, plan hash, Change Review verdict, adversarial
  verdict, tests/checker/baseline, changed paths, known limitations, and current-main identity.
  Publication requires a separate owner decision. Push one exact reviewed branch and create one PR;
  merge remains manual.

- [ ] **Step 5: require post-merge distinct FINAL**

  After manual merge, a new `gpt-6-astra/high` FINAL reviews the complete integrated Module 4 at exact
  current main, reruns fresh checks from a clean archive, pressure-tests the bounded scanner pipeline,
  and verifies no drift after its verdict. Only `FINAL_PASS` with no Critical/Important finding on
  unchanged main permits Module 4 `DONE`.

## Acceptance Criteria

1. All historical C03 reproducers have named end-to-end regressions through real C03; representative
   failures also have full subprocess CLI evidence.
2. Whole supported images are consumed, emit no link destination, and never hide adjacent links.
3. Every supported link emits exactly one candidate; positives prove observation rather than relying
   on PASS alone.
4. Recognized malformed bounded syntax fails C03 and cannot become an exemption.
5. Existing destination classification, filesystem boundaries, output schema, evidence redaction,
   C01–C12 order, and baseline integrity remain unchanged.
6. Full suite and mutation checks pass on the exact candidate; evidence records exact identities and
   does not claim complete bug absence, behavioral proof, installation, or release readiness.
7. Independent Change Review and independent adversarial review both PASS the exact unchanged head
   before publication is requested.
8. Manual merge and a new distinct FINAL on unchanged main remain mandatory.

## Risks and Controls

- **Another interaction gap:** wrapper × context × destination matrix, token observability, mutation
  checks, and pre-publication adversarial review target cross-effects rather than isolated examples.
- **Accidental parser expansion:** explicit grammar and non-goals; no dependency or advanced syntax.
- **Image regression:** link and image share bounded payload parsing, but only links enter classifier.
- **False PASS on malformed input:** recognized malformed constructs emit invalid tokens and fail C03.
- **False FAIL on valid bounded input:** paired target-dependent positives cover labels, angle/plain
  destinations, titles, `)`, spaces, images, and adjacency.
- **Infinite loop or nondeterminism:** every scanner path advances; repeated CLI output must be byte-
  identical; evidence remains sorted and deduplicated.
- **Review overconfidence:** green tests and review counts are evidence for named cases only; FINAL
  remains independent and post-merge.
- **Scope creep:** any need for a dependency, public contract change, new syntax, or other C-check
  pauses implementation and returns options to Product.

## PLAN Review and Authorization Boundary

An independent `gpt-5.6-sol/high` PLAN reviewer checks this entire file against the binding sources,
exact base, current implementation, all recorded findings, and owner-approved constraints. It must
assess supported grammar clarity, whole-construct design, historical coverage, TDD sequencing,
review independence, permission boundaries, and whether the plan avoids both regex patching and a
general Markdown parser.

`PLAN_PASS` binds the computed SHA-256 of this file and exact base
`939980ded8fb2be14fb8e5a32c3302f5ad56fd33`. Any change invalidates it. After PLAN_PASS, the Task
coordinator presents a simple explanation and the identity-bound package to the owner in this Task.
Owner acceptance authorizes only local Implementation and the stated pre-publication reviews; it does
not authorize push, PR, merge, installation, publication, pilot, release, or Module 5.

Structural checks do not prove behavioral correctness.
