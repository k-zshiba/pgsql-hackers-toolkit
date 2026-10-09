# Validation and self-review

Package verification date: 2026-10-09; initial runtime/URL evidence: 2026-10-06.
This file records the tested unreleased v0.1.0,
scope and material limitations. Do not replace missing evidence with claims.

## Toolchain and scope

APM CLI 0.33.0; maintainer tests use Python 3.11. All APM work happens in
temporary author/consumer projects with isolated child-process homes. No global
agent environment, live database or user PostgreSQL checkout is modified.
The implementation does not publish a tag or send contributor mail.

## Verification record

| Check | Observed result |
| --- | --- |
| `python -m unittest discover -s tests -v` | 12 tests passed: five structural, four real APM integration and three eval-contract tests |
| `python evals/grade.py --validate` | 19 scenarios valid: nine positive, six negative and four safety cases; all seven Skills covered |
| Official Skill creation validator | All seven Skill frontmatters passed |
| APM author loop | Frozen install, manifest/instruction validation, dry-run and actual compilation, CI audit and plugin ZIP pack succeeded in isolated source copies |
| Consumers | Eight scenarios: Codex, Claude, Copilot and portable Agent Skills individually, all three provider pairs and the three-provider combination; source content/metadata and relative references verified |
| Idempotency and reproducibility | Second frozen install/compile retained byte snapshots; tagged Git fixture locked exact commit and replayed after its package cache was removed |
| Drift and ownership | Changed manifest ref rejected without deployment mutation; changed deployed Skill and Copilot instruction detected by audit; prune preserved user Claude/Copilot rules and a GitHub workflow; recompilation removed obsolete Codex context |
| Packed artifact | Seven Skills, their references, shared instruction, byte-matched PostgreSQL License notice, SPDX metadata and integrity hashes checked; tampered bundle refused installation |
| Offline Codex runtime | Codex CLI 0.159.2 `skills/list` recognized all seven enabled Skills with no errors; zero model turns |
| Source URL checks | 64 research and Skill-source URLs reachable; corrected a stale OpenAPM URL during review |

The optional runtime check is reproducible with:

```bash
python tests/check_codex_runtime.py --codex /path/to/installed/codex
```

It uses the official [app-server handshake and skills/list API](https://learn.chatgpt.com/docs/app-server),
only initialization and read requests, a fresh consumer and disposable
`HOME`/`CODEX_HOME`. No authentication, conversation or model request is made.
Claude CLI 2.1.133 was available, but authenticated runtime Skill discovery was
not exercised; the Claude integration evidence is deployment inspection.
Copilot deployment was rechecked on 2026-10-09 using APM 0.33.0. Copilot CLI
was not installed, so no Copilot runtime discovery or live model run is claimed.

## Critical self-review

Reviewed from both a PostgreSQL contributor's and a package maintainer's
perspective. This is author self-review, not an independent human review.

- **Contributor scope:** excluded SQL/operations intents in all relevant routing
  descriptions and in six negative fixtures. No static subsystem facts, frozen
  branch-support lists, fabricated commands or ready-for-submission guarantees.
  Current source, whole discussion, relevant tests and unresolved evidence guide
  each workflow. Backpatch assessment is branch-specific.
- **Community and safety:** large undiscussed features route to research/design;
  mirror PRs are not the contribution route. Dirty/untracked work, separate
  applicability experiments, actual test evidence and explicit external-write
  authorization are required. These instructions cannot enforce agent permissions.
- **Packaging:** kept one package, no external agent dependencies, unnecessary
  agents or handwritten provider adapters. Found producer-target restrictions
  blocking portable consumers and added `agent-skills`. Distinguished validation,
  compilation, packing and supported native Git installation.
- **Upstream defects:** discovered direct-bundle link relocation and instruction
  discovery problems, the dependency-free legacy pack defect and Python 3.10
  audit failure. Documented the supported path instead of implementing another
  installer or duplicating contributor rules. Added a tested legal notice inside
  packed primitives because root license files are not packable includes.
- **Ownership and documentation:** verified native relative links and generated
  content against canonical source, without committed deployed copies. Added
  recompilation after prune to remove stale root context. Removed leftover
  scaffold prose; synchronized README, examples and release policies.
  Copilot-only consumers contain no Claude artifacts, Codex root or duplicate
  Skill tree; combined consumers share `.agents/skills/`.
- **Eval honesty:** scenario and grader tests validate the evaluation mechanism;
  they do not establish model routing performance. Offline Skill listing proves
  discovery only. Kept live observations opt-in and separated these claims.

## Known upstream constraints

- APM 0.33.0's audit scanner imports `tomllib`, failing under Python 3.10 in the
  tested environment. Use Python 3.11+ for full validation.
- Legacy `apm pack --format apm` emits an empty bundle for this dependency-free
  package. Default plugin format includes the canonical Skills/instructions and
  is our tested packed path.
- Direct bundle deployment needs an explicit `--target` in the tested CLI.
  Git package installation uses the consumer's manifest targets normally.
- Even with explicit targets, direct plugin-bundle deployment does not relocate
  cross-Skill links to shared instructions. Plugin-directory dependencies resolve
  these links but omit root instruction discovery. Neither is a supported full
  consumer install path for this release; native `.apm/` packages work correctly.
  Packed contents and integrity are tested separately from native installation.
- Run install/compile before pack in an isolated source copy. Packing an
  uninstalled copy can emit `pack.target: minimal`, which 0.33.0 then fails
  to normalize during bundle install. The tested producer loop avoids this
  upstream path without patching APM or editing packed locks.
- Frozen install checks manifest/lock agreement; content drift requires audit.
  Local path dependencies are not commit-pinned; Git fixtures exercise replay.
- Prune removes owned Skills/rules, but compiled Codex context remains until
  recompilation. Root license text is rejected as an explicit primitive include;
  the package therefore carries a tested matching notice inside instructions.

## Limits

Artifact paths, metadata and contents are validated; offline Codex discovery is
verified separately. Authenticated Claude/Copilot discovery, loaded instruction behavior
and live LLM routing are not implied by these tests. The published repository/tag
install smoke test remains
a release-time check. No PostgreSQL patch was built by this toolkit task, so no
PostgreSQL build/test result is claimed.

Next validation priorities: reviewed live-agent routing traces, an immutable
public-tag cold install after an authorized release, and rechecking upstream
bundle/agent compatibility when upgrading APM. No marketplace infrastructure or
additional dependency is needed for these steps.
