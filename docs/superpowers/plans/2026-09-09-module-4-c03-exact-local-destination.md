# Module 4 C03 Exact Local Destination — Plan Addendum

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:subagent-driven-development` and
> `superpowers:test-driven-development`. Do not begin Implementation until the owner accepts this
> exact addendum identity.

**Identifier:** `MODULE4-C03-DESTINATION-ADDENDUM-v1`. Identity is this file's SHA-256 plus the exact
base below. Any content or base change invalidates `PLAN_PASS`.

**Goal:** preserve the exact local path emitted by the accepted bounded inline scanner through C03
classification, query/fragment removal, and filesystem validation, so URL parsing cannot silently
validate a different path.

**Architecture:** keep the scanner and supported grammar unchanged. Add one private destination
classification boundary that recognizes schemes and network paths only at string index zero, then parses
scheme-free local destinations behind a non-whitespace sentinel so `urlsplit` cannot remove leading
spaces. It returns either an exempt destination, an invalid destination, or the exact local path
after the existing query/fragment semantics. Existing containment, symlink, regular-file, evidence,
CLI, and other C-check behavior remains unchanged.

**Tech stack:** Python 3 standard library, current checker/test interfaces, Git.

**Binding sources:** `SPEC.md` §§6–10 and §12; parent `MODULE4-PLAN-v1`; accepted
`MODULE4-C03-REPLAN-v1`; post-merge FINAL finding on exact main
`d17cef47c8ea491fd0e16c588f12b2e3bb06dbb9`.

## Identity, authority, and scope

- Exact base/current main: `d17cef47c8ea491fd0e16c588f12b2e3bb06dbb9`, freshly verified from PR #9,
  `FETCH_HEAD`, and `origin/main` on 2026-09-09.
- Parent plan SHA-256: `0ee46fce6779021b3d41238af6902a191bbba697e349fb8bfcc3150190658246`.
- Bounded-scanner plan SHA-256:
  `c377e374b88e31bdf56788f55f4db9f02cdedaae5c810579e3275741c640a44c`.
- This addendum supersedes only the earlier constraint that C03 destination classification remain
  byte-for-byte unchanged. Product explicitly authorized planning this bounded identity-preservation
  correction after FINAL. All scanner grammar, token, recovery, and image decisions remain binding.
- Future candidate paths are exactly this addendum, `scripts/check_workflow.py`, and
  `tests/test_check_workflow.py`.
- No dependency, grammar expansion, URI decoding, remote lookup, C01 or other C-check change, public
  API, installation, release, Module 5, push, PR, or merge is authorized by plan approval.
- Planning/PLAN review: `gpt-5.6-sol/high`; Implementation: `gpt-5.6-sol/medium`; exact-head Change
  Review: `gpt-5.6-sol/high`; pre-publication adversarial review and post-merge FINAL:
  `gpt-6-astra/high` in distinct sessions.
- Required limitation: `Structural checks do not prove behavioral correctness.`

## Root cause and exact contract

The bounded scanner correctly emits `InlineConstruct("link", " references/lifecycle.md")` for:

```markdown
[](< references/lifecycle.md>)
```

The current classifier calls `urlsplit(destination)`. Python removes leading ASCII space before
parsing, so `parsed.path` becomes `references/lifecycle.md`. C03 validates that different existing
file and falsely reports PASS. The paired case with a real literal file named ` proof.md` falsely
reports FAIL. This is a lossy classification boundary, not a scanner defect.

The corrected private classifier must implement this order:

1. Reject only a raw `destination == ""`. Do not apply local-path emptiness rules before fragment
   and scheme classification; pathless `http:`, `https:`, `mailto:`, and `#` remain eligible for
   their existing exemptions.
2. Recognize fragment-only input exactly as today: the raw destination begins with `#` and has no
   scheme, authority, path, or query. Keep it exempt.
3. Recognize a URI scheme only when the raw destination begins at index zero with the ASCII scheme
   production `[A-Za-z][A-Za-z0-9+.-]*:`. Parse that exact value with `urlsplit`; exempt only
   case-insensitive `http`, `https`, and `mailto`; reject every other scheme or parse error.
4. Reject a network-path authority only when the raw destination begins exactly with `//`.
5. For every remaining scheme-free relative destination, parse `"./" + destination` with
   `urlsplit`. The sentinel prevents leading-space removal. Require no parsed scheme or authority,
   remove exactly the two sentinel characters from `parsed.path`, and use the remaining text as the
   local filesystem path. After this parse, reject the local path when it is empty or contains only
   U+0020 spaces. This post-parse rejection covers query-only, leading-space-before-query/fragment,
   and whitespace-only local inputs. Query and fragment otherwise remain excluded exactly as before;
   no percent-decoding, trimming, Unicode normalization, case folding, or separator rewriting occurs.
6. Apply the existing absolute-path, containment, symlink-component, and regular-file checks to that
   exact local path. A leading space before `/`, `//`, `http:`, or another scheme-like substring is
   therefore part of a relative local path, not an exemption or authority.

Within the accepted one-line grammar, explicitly characterize every lossy `urlsplit` behavior that
could change identity: one or multiple leading spaces; leading space before allowed/unsupported
scheme-like text, `//`, `#`, or `?`; inner/trailing spaces; query/fragment removal; mixed-case schemes;
empty and whitespace-only angle destinations. Controls remain rejected by the scanner and are not a
new classifier input.

Suggested private interface:

```python
@dataclass(frozen=True)
class ClassifiedDestination:
    kind: Literal["exempt", "local", "invalid"]
    local_path: str | None


def _classify_inline_destination(destination: str) -> ClassifiedDestination:
    """Classify without changing the identity of a local path."""
```

The exact private shape may be simplified if the same three states and order remain directly
testable. The scanner must not read the filesystem; the classifier must not inspect labels, titles,
or image targets.

## TDD matrix

Every row uses literal scanner-token expectations and a fresh copied root for direct C03. The two
load-bearing raw-path pairs also run through the real CLI.

| ID | Raw destination | Fixture | Expected classification / C03 |
|---|---|---|---|
| D01 | ` references/lifecycle.md` | stripped path exists; exact path missing | local exact / FAIL |
| D02 | ` proof.md` | exact leading-space file exists; stripped path missing | local exact / PASS |
| D03 | `  proof.md?mode=1#part` | exact two-space file exists | query/fragment removed, spaces preserved / PASS |
| D04 | `references/proof file.md`; same path plus trailing space | inner-space file exists; trailing-space target missing | local exact / PASS then FAIL; trailing space retained |
| D05 | one or more spaces only, including `< >` | no fixture | invalid / FAIL |
| D06 | `http:`, `https:`, `mailto:` at index zero, mixed case included | no local file | exempt / PASS |
| D07 | `ftp:`, `file:`, arbitrary scheme at index zero | classifier assertion; no colon-bearing file required | invalid / FAIL |
| D08 | `//host`, `//host/path` at index zero | any | invalid / FAIL |
| D09 | leading space before `https:`, `ftp:`, or `//host` | exact classifier assertion; local path missing | local exact / FAIL, never exempt/authority |
| D10 | `#`, `#part`, `#part?query` at index zero | any | fragment-only / PASS |
| D11 | leading space before `#part` or `?query` | no fixture | invalid after exact suffix removal / FAIL |
| D12 | ordinary local path with query/fragment | existing then missing | existing semantics / PASS then FAIL |
| D13 | absolute, escape, directory, leaf/ancestor/dangling symlink | bounded fixtures | existing filesystem contract unchanged / FAIL |
| D14 | valid image with leading-space target plus adjacent link | adjacent valid then missing | image ignored; adjacent link observed / PASS then FAIL |
| D15 | `http://[` | no fixture | scheme parse error becomes invalid / direct C03 and CLI FAIL only C03 |
| D16 | `references/name:part.md?x#y` | classifier assertion; local target missing | local `references/name:part.md` / direct C03 FAIL |

Colon-bearing fixture guidance is platform-safe: D07 and D16 assert the private classifier identity
directly and do not create colon-bearing filenames on platforms that prohibit them. POSIX-only file
creation is neither required nor sufficient for these branches.

D11 directly asserts `kind="invalid"` and `local_path=None` for both forms; neither form may reach a
whitespace-only filesystem lookup.

Required CLI pairs:

- D01 must exit `1`, fail only C03, retain ordered twelve-check output and limitation, and disclose
  neither root nor raw/stripped destination.
- D02 must exit `0` with C01–C12 PASS, proving the exact leading-space file can resolve.
- D15 must exit `1` with a complete structured response, only C03 failed, empty stderr, and no raw
  destination disclosure; the classifier must return `invalid` rather than leak `ValueError`.
- Repeat D01 twice and require byte-identical stdout.

Required mutation checks:

- replace the exact local-path result with direct `urlsplit(destination).path`;
- strip or `lstrip` the local path;
- remove the sentinel before local parsing;
- stop removing query/fragment;
- treat whitespace-only as a file path, including whitespace left after removing a query or fragment;
- accept a leading-space scheme-like value as an exemption;
- remove scheme parse-error handling or search for a scheme beyond string index zero;
- reject a colon in a later local path component as though it were a scheme;
- remove existing scheme, network-path, containment, or symlink guards.

At least one named test must fail for each mutation. Restore every mutation before committing.

## One bounded work item

1. Create an execution branch from exact base and carry this accepted addendum unchanged; verify its
   hash and that it is the only untracked path.
2. Add RED classifier/unit, scanner-token, direct-C03, and CLI tests for D01–D16. Run direct/CLI RED
   separately from any missing new helper interface so both false PASS and false FAIL are observed.
3. Implement the smallest private classification boundary above and route link tokens through it.
   Do not change scanner code or other C-checks.
4. Run focused GREEN, mutation checks, full tests, C01–C12 checker, baseline 7/7, plan hashes,
   base-to-head whitespace/path checks, and status checks. Stage exactly the three authorized paths
   and create one local candidate commit. No push or PR.
5. A fresh read-only `gpt-5.6-sol/high` Change Reviewer examines the exact full candidate. Corrections
   invalidate the verdict and repeat full review.
6. After Change Review PASS, a distinct read-only `gpt-6-astra/high` adversarial reviewer constructs
   fresh transformation and raw-path pairs, observes classifier output plus direct C03/CLI behavior,
   and returns `ADVERSARIAL_PASS` only with no Critical/Important finding on unchanged head.
7. Repeat coordinator verification and stop for separate publication authorization. Merge remains
   manual. A new distinct post-merge FINAL on exact unchanged main remains mandatory for Module 4
   `DONE`.

## Acceptance criteria and risks

- Exact scanner-emitted local path identity reaches filesystem validation after only the documented
  query/fragment removal; D01 and D02 prove both directions of the former defect.
- Existing allowed-scheme, fragment-only, unsupported-scheme, network-path, empty/whitespace,
  absolute, containment, directory, and symlink semantics remain unchanged.
- Images remain excluded and cannot hide adjacent links. Scanner grammar and recovery remain
  unchanged.
- CLI evidence remains deterministic, repository-relative, destination-redacted, and complete.
- Risk of another parser normalization is controlled by explicit transformation characterization,
  paired exact-path fixtures, and mutation-sensitive tests.
- Risk of scope creep is controlled by the three-path boundary and prohibition on grammar,
  dependency, other-check, or public-contract changes.
- Green tests and review counts establish only the named structural cases. They do not prove absence
  of all bugs, behavioral readiness, installation, or release readiness.

## PLAN review and authorization boundary

A distinct `gpt-5.6-sol/high` PLAN reviewer checks this complete addendum against exact main, both
accepted plans, the FINAL reproducer, current code/tests, and binding product constraints. PASS
requires no unresolved Critical or Important finding and binds the exact base plus this file hash.

After `PLAN_PASS`, present the owner the cause, the identity-preserving approach, D01/D02 proof,
scope, risks, and exact identity in this Module 4 Task. Owner acceptance authorizes only local
Implementation and stated reviews. It does not authorize push, PR, merge, installation, release, or
Module 5.

Structural checks do not prove behavioral correctness.
