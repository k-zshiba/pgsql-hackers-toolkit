# Contributing

Contribute verifiable PostgreSQL **core contributor workflows**, not a static
internals encyclopedia or database usage advice. Keep agent artifacts original,
small and routed by task intent. [Architecture](docs/architecture.md) describes
the authoring boundary; [research](docs/research.md) records official sources.

## Changes and validation

Author only in `.apm/instructions/` and `.apm/skills/` for agent artifacts.
Do not edit/commit deployed AGENTS.md, CLAUDE.md, provider trees or plugin
manifests. One common instruction owns shared rules. Keep intra-Skill references
local; check package-relative links after installation. APM owns all transforms.
Copilot's `.github/instructions/` and `.github/copilot-instructions.md` are
generated artifacts too; `.github/workflows/` remains maintained CI source.
No new adapter, subagent or executable helper without a concrete need.
Keep `.apm/instructions/LICENSE` byte-identical to root `LICENSE`; this legal
notice accompanies packed primitives because APM cannot pack a root license
through its primitive allowlist. Tests enforce both the source match and ZIP notice.

Use Python **3.11+** for maintainer validation. APM 0.33.0 advertises Python 3.10
support, but its audit file scanner imports `tomllib` on the tested release.

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python evals/grade.py --validate
```

The integration suite copies source to temporary author and consumer projects.
It executes `apm compile --validate`, dry-run/actual compile, frozen install,
audit, pack and install using the pinned released CLI. APM creates its own
temporary global config/cache in isolated child-process homes. The real user's
home and PostgreSQL checkout are not mutated.

To explore the verify loop manually, **in an isolated source copy**:

```bash
apm install --frozen
apm compile --validate
apm compile --dry-run
apm compile --single-agents
apm audit --ci
apm pack --archive -o dist
```

Root lock maintenance uses `apm lock` before deployment, so the committed lock
records only the empty external dependency closure rather than generated local
deployment metadata. If dependencies are introduced, review actual resolved
commits, transitive dependencies, licenses and hashes; do not hand-edit the lock.

Add routing fixtures for behavior changes, including likely false positives.
Fixture/grade validation is not live routing evidence. For a substantial change,
run the [optional real-agent eval procedure](evals/README.md) and retain model,
client, package revision and transcript evidence. Report unperformed checks.
Do not hard-code a live PostgreSQL source revision, test command, supported
branch list or CommitFest manager into the workflows.

## Versioning and releases

Use Semantic Versioning with `apm.yml` as package version authority and Git
tags named `vMAJOR.MINOR.PATCH`. Keep examples and CHANGELOG in agreement.

| Change | v0.x policy |
| --- | --- |
| Wording/source-link fix preserving behavior | Patch release |
| Skill/instruction correction preserving public scope and safety contract | Patch release; describe changed behavior |
| New Skill or changed routing/workflow contract | Minor release, eval coverage and compatibility notes |
| Skill rename/removal, layout/install-path change, stronger/different invocation requirements | Minor release with migration instructions; never silently break in a patch release |
| Post-1.0 incompatible public behavior | Major release |

After 1.0, additive compatible behavior is minor, compatible fixes are patch,
and breaking names/behavior/layout are major. During v0.x compatibility is
guaranteed within a minor line to the tested installation/workflow contract;
minor upgrades can break and must be reviewed. Upgrading APM is not an automatic
toolkit behavior change: repeat consumer/pack tests and record new compatibility.

Release procedure:

1. Recheck APM and agent official docs if changing package/deployment behavior.
   Set the package version; update CHANGELOG and example dependency refs.
2. Run all tests/eval validation and critical self-review. Inspect the packed ZIP,
   canonical/deployed links and final Git diff. The tag must include `.apm/`,
   manifest, lock, docs and license. No generated deployment files.
3. Prepare a concrete release/tag and description for maintainer approval. Local
   preparation does not authorize pushing tags, uploading assets or marketplace
   publication. Once explicitly authorized, publish an immutable SemVer tag on
   the Git repository; no independent registry is needed.
4. Smoke-test the **published** `k-zshiba/pgsql-hackers-toolkit#vX.Y.Z` from a
   fresh consumer, commit its lock in that consumer and replay a cold frozen
   install. Local Git fixtures test mechanics but cannot prove public availability.

Marketplace registration is optional discovery. APM can synthesize plugin
metadata from the manifest; don't create a parallel handwritten plugin source.

## Dependency policy

v0.1 has zero external agent-artifact dependencies, including devDependencies,
MCP and LSP. Before adding one, explain why its value cannot be provided by a
small original local workflow. Core contribution must still work if a nonessential
external Skill disappears. Record:

- Source, exact version/ref and resolved commit/hash.
- Declared license and actual licensing/notice obligations.
- Maintenance/release status, owner and update plan.
- Full transitive closure and necessity of every executable/MCP/hook surface.
- Permissions, network/credential behavior, supply-chain and disappearance risk.

Declare accepted dependencies in `apm.yml`, generate `apm.lock.yaml` through APM,
and verify fresh frozen install plus audit in CI. Do not implement another
resolver or hide downloads in scripts. Dev-only artifacts belong outside shipped
source and in explicit devDependencies if genuinely needed.

APM CLI is the one directly pinned development tool in `requirements-dev.txt`.
Its Python dependencies are owned by upstream and are not locked by apm.lock;
this repository does not claim full Python-toolchain byte reproducibility. CI
uses Python 3.11 and pinned official checkout/setup-python/upload-artifact v7
action revisions (MIT, Node 24, GitHub-hosted Ubuntu runner). Review upstream license (MIT),
security advisories and dependency changes before upgrading. No third-party
reference-project prose/code is copied into our package.

## Review criteria

Check core/application separation, current-source evidence, inference handling,
prior discussion, dirty-tree preservation and external-write authorization.
Challenge reviewer reassurance and unverified test/readiness claims. Check Skill
boundaries, negative evals, source/deployment duplication, pack contents and
README accuracy. Do not approve a workflow based only on Markdown lint.

Toolkit contributions use this repository's normal review mechanism. PostgreSQL
patches produced with it follow PostgreSQL's own current pgsql-hackers/CommitFest
process. They are separate projects and separate submission decisions.
