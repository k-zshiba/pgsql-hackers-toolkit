# Validation

Package verification: 2026-10-09; runtime/URL evidence: 2026-10-06.
Unreleased v0.1.0, APM 0.33.0 and Python 3.11; temporary projects with isolated homes.

## Recorded results

| Check | Result |
| --- | --- |
| Unit/integration suite | 12 passed: five structure, four APM integration, three eval-contract tests |
| Eval fixtures | 19 valid: nine positive, six negative, four safety cases; all seven Skills covered |
| Skill metadata | All seven frontmatters passed the Skill creation validator |
| APM author loop | Frozen install, validation, dry-run/actual compilation, audit and ZIP packing passed |
| Consumers | Eight scenarios: Codex, Claude, Copilot and portable Agent Skills individually, all provider pairs and the three-provider combination; contents and links checked |
| Reproducibility | Repeat install/compile preserved bytes; tagged Git fixture replayed the locked commit after cache removal |
| Drift/prune | Ref drift rejected; Skill/Copilot rule changes detected; user Claude/Copilot rules and GitHub workflow preserved; recompile cleared pruned Codex context |
| Archive | Skills, references, shared instruction, matching license and integrity hashes checked; tampering rejected |
| Codex discovery | CLI 0.159.2 listed seven enabled Skills without errors or model turns |
| Source links | 64 research/Skill URLs reachable at verification time |

Run the current suite using [CONTRIBUTING](../CONTRIBUTING.md#edit-and-test).
Optional read-only Codex discovery, using an installed CLI:

```bash
python tests/check_codex_runtime.py --codex /path/to/installed/codex
```

This check creates a disposable consumer and agent home and makes no authentication
or model request.

## APM 0.33.0 constraints

- Full validation requires Python 3.11+: the audit scanner imports `tomllib`.
- Copilot-only consumers omit compilation; `--single-agents` emits redundant Codex
  context. Combined targets compile only when Codex is selected.
- Use native Git/local-source packages for installation. Direct ZIP deployment
  breaks links to shared instructions; plugin-directory dependencies omit root
  instruction discovery. ZIP contents and integrity are tested separately.
- Use default plugin packing. Legacy `apm pack --format apm` emits an empty bundle
  for this dependency-free package; portable `agent-plugin` cannot carry instructions.
- Install and compile in an isolated copy before packing to avoid an unsupported
  `pack.target: minimal` lock. Direct bundle deployment also needs explicit targets.
- Frozen install checks manifest/lock agreement; audit checks deployed content.
  Local-path dependencies are not pinned to Git commits.
- After pruning, recompile to remove stale Codex root context. The packed license
  must live inside the primitive directories.

## Coverage limits

Author self-review checked contributor scope, evidence, safety, packaging and eval
claims. This was not independent review. Package checks and offline discovery
do not prove loaded instruction behavior or live model routing. Authenticated
Claude/Copilot discovery, public-tag cold installation and live-agent evals remain open.
No PostgreSQL patch was built or tested. Recheck compatibility on APM upgrades.
