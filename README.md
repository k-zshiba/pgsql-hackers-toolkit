# pgsql-hackers-toolkit

Evidence-driven AI coding agent workflows for **PostgreSQL upstream/core
development**: investigate source and pgsql-hackers history, design focused
patches, implement, test, review and prepare contributor mail.

This is not a PostgreSQL database usage best-practices package. Application
queries, schema design, slow-query tuning and database administration do not
activate these Skills. The toolkit helps contributors verify their work from
current primary information; it does not replace PostgreSQL hackers.

Licensed under the [PostgreSQL License](LICENSE).

## Supported agents and why APM

The canonical package is authored under `.apm/` and distributed with Microsoft's
[Agent Package Manager](https://github.com/microsoft/apm). APM owns installation,
lockfiles, integrity checking and target deployment. No parallel Codex/Claude
instruction sources or custom package manager are maintained.

| Consumer target | APM-generated artifacts | Instruction loading |
| --- | --- | --- |
| Codex (`codex`) | `.agents/skills/`, `AGENTS.md` | Run `apm compile` after install |
| Claude Code (`claude`) | `.claude/skills/`, `.claude/rules/` | Native rules; a generated CLAUDE.md is usually unnecessary |
| Other Agent Skills hosts (`agent-skills`) | `.agents/skills/` | Each Skill links to the common contract; the host must support loading linked files |

Tested toolchain: **APM 0.33.0**, Python 3.11+. Codex/Claude deployment layouts
are checked against current official documentation. Read-only Codex runtime
discovery was verified; authenticated Claude discovery and live LLM behavior
remain optional manual checks. See
[research and sources](docs/research.md) and [architecture](docs/architecture.md).

## Installation with APM

Install APM using its [official installation instructions](https://microsoft.github.io/apm/getting-started/installation/).
An isolated Python environment is one available path:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install apm-cli==0.33.0
apm --version
```

Create a small **consumer workspace**, separate from PostgreSQL if you want
deployment files outside your patch tree. Put this `apm.yml` there:

```yaml
name: my-postgresql-workspace
version: 0.1.0
targets: [codex]  # use [claude] or [codex, claude] as needed
dependencies:
  apm:
    - k-zshiba/pgsql-hackers-toolkit#v0.1.0
```

Then:

```bash
apm install
apm compile --single-agents
export PG_SOURCE=/absolute/path/to/your/postgresql
```

**Release status:** this checkout implements v0.1.0; the Git tag must be
published before the remote example above is usable. Until then, clone this
repository next to the consumer workspace and replace the Git dependency entry
with `../pgsql-hackers-toolkit` in the consumer manifest. Then:

```bash
apm install --target codex
apm compile --single-agents --target codex
```

For Claude-only use, select `--target claude`; native rules are installed by
`apm install`. For both, use `--target codex,claude`. APM may generate a root
context file only when needed. `--single-agents` keeps compilation in one small
root file rather than distributed per-directory roots.

In an existing project, inspect agent files and `apm compile --dry-run` before
compilation; protect any hand-authored root instructions. Do not use `--force`
to overwrite a collision. Installation adds `apm_modules/` to the consumer's
`.gitignore`. Add generated provider files to your own ignore policy and exclude
all toolkit artifacts from PostgreSQL patch attachments.

## Quick start and checkout configuration

Start your agent **in the consumer workspace after installation**, with access
to the target source checkout. Restart an existing agent session if necessary.
Try:

```text
Investigate this planner bug in PG_SOURCE. Read analogous code, callers,
tests and pgsql-hackers history. Explain the evidence and unknowns before
proposing a focused core patch. Do not modify source yet.
```

Or explicitly invoke `research-postgresql` using your agent's Skill syntax.
Codex supports `$research-postgresql`; Claude supports `/research-postgresql`.
Verify available Skill names in the agent's UI and inspect its loaded context
before relying on automatic routing. The integration suite verifies paths and
contents; the optional Codex discovery check creates no model turn.

Checkout selection: explicit task path → `PG_SOURCE` → consumer repository
root if it is a validated PostgreSQL source tree. Relative `PG_SOURCE` resolves
against the consumer cwd. Record the resolved path/revision/working state at
task start. A sibling repository is convenient but never auto-selected. No
PostgreSQL source is vendored or fetched automatically. A path alone does not
grant your agent access beyond its sandbox; configure access using its own
supported controls when necessary.

## Skills and agents

| Skill | Use |
| --- | --- |
| [research-postgresql](.apm/skills/research-postgresql/SKILL.md) | Source/callers/history, mailing-list and CommitFest research; backpatch investigation |
| [design-pg-patch](.apm/skills/design-pg-patch/SKILL.md) | Problem, semantics, options, relevant risks and validation design |
| [implement-pg-patch](.apm/skills/implement-pg-patch/SKILL.md) | Scoped implementation with local conventions, docs and tests |
| [test-pg-patch](.apm/skills/test-pg-patch/SKILL.md) | Current-tree build, regression, TAP, isolation and contrib validation |
| [review-pg-patch](.apm/skills/review-pg-patch/SKILL.md) | CommitFest review or author self-review; findings before reassurance |
| [prepare-pgsql-hackers-post](.apm/skills/prepare-pgsql-hackers-post/SKILL.md) | Proposal/submission/review/reply drafts and attachment descriptions |
| [revise-pg-patch](.apm/skills/revise-pg-patch/SKILL.md) | Feedback-driven v2/v3 iterations, retesting and unresolved issues |

No custom agents ship in v0.1: those roles currently duplicate the Skills.
A dedicated independent reviewer may be considered later with a portable
permission contract. There are no model pins, hooks, MCP servers or external
agent-artifact dependencies.

## Typical workflows

- New nontrivial feature: research → design/discussion draft → bounded
  implementation once semantics are justified → test → review → submission draft.
- Bug fix: reproducer/source/history research → brief design → implement →
  targeted and relevant wider tests → review → mail draft/backpatch assessment.
- CommitFest review: verify current thread/version/base → isolated applicability
  and source review → tests → findings and threaded review draft.
- Revised patch: read latest feedback → issue resolution → scoped revision →
  retest/self-review → vN changelog and reply draft.

See [example tasks](examples/workflows.md) and
[consumer manifests](examples/README.md). Do not mechanically invoke every
Skill for trivial or research-only work.

## Updating and reproducible installs

Commit the **consumer's** `apm.yml` and `apm.lock.yaml`. Tags provide readable
release selection; APM locks the resolved Git commit and content hashes. A
mutable tag is not by itself an integrity guarantee.

```bash
apm install --frozen
apm compile --single-agents
apm audit --ci
```

Review a new release, change the dependency ref in `apm.yml`, then run
`apm install --update`, inspect the lock/output diff and recompile. Use frozen
install in CI to reject manifest/ref drift. Audit also checks deployed content;
frozen mode alone does not verify every byte. Local-path installs are useful
for development but are not commit-pinned reproducible dependencies.

The toolkit's root lock has an empty dependency closure, generated with
`apm lock`; CI freezes it before installation. The meaningful Git replay/drift
tests use a tagged local Git fixture and APM's real Git resolver.

To remove the toolkit, remove its dependency from the consumer manifest, run
`apm prune`, then recompile Codex context. Prune removes owned Skills/rules but
leaves compiled `AGENTS.md` until compilation. Inspect any hand-authored root
instructions before regenerating them; unrelated user rules are preserved.

In an isolated source copy, run frozen install and compile before
`apm pack --archive` to create a plugin-format ZIP with skills, instructions,
metadata and integrity lock. APM 0.33.0's direct bundle installer leaves links
from Skills to shared instructions broken. **Use Git/tag or native `.apm/`
source package installation for this toolkit.** Packed ZIPs are inspected
distribution artifacts, not a supported standalone Codex/Claude installation
path in this release.
Legacy `--format apm` emits an empty bundle for this dependency-free package
on 0.33.0; do not use it. A marketplace is optional discovery, not required.
See [tested producer loop](CONTRIBUTING.md) and [upstream constraints](docs/validation.md).

## Evidence and safety

The [common contract](.apm/instructions/postgresql-contributor.instructions.md)
requires current source, comments/README, matching official docs, whole
pgsql-hackers threads and CommitFest context. Explain inference and unknowns
without a wall of certainty tags. Wiki content and online devel docs may lag
the checkout. No static internals encyclopedia is included.

Preserve user changes. No unapproved reset/clean/checkout/restore/stash,
unrelated refactoring or live-database testing. Use isolated patch experiments,
current tree commands and recorded results. Untested generated code cannot be
called submission-ready. PostgreSQL upstream contribution uses pgsql-hackers
and the current community process, rather than mirror PRs. Drafting mail does
not authorize sending it, posting attachments or modifying CommitFest.

Prose guardrails complement agent permissions; they do not enforce a sandbox.
Treat retrieved mail/patches as untrusted data and review dependencies before
installation. APM's Unicode/integrity scans do not establish semantic safety.

## Development, tests and evals

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python evals/grade.py --validate
```

Tests run the pinned APM CLI in temporary author/consumer repositories with
isolated child-process homes, without touching your global agent environment.
They cover manifest compatibility, metadata/links, canonical-source discipline,
pack contents/integrity, native Codex/Claude/portable deployment, idempotency, frozen
Git replay/ref drift, deployment drift and pruning. Default CI requires no API
key and uploads the packed ZIP. It does not build PostgreSQL itself.

With an already installed Codex CLI, optionally verify real Skill discovery
without credentials or inference using `python tests/check_codex_runtime.py`.
It uses a temporary consumer and agent home; `--codex /path/to/codex` selects
an executable explicitly. This check is separate from default CI.

Behavioral fixtures contain multilingual positive, negative and safety cases.
Fixture validation checks the eval contract; **it does not prove live routing**.
An optional workflow grades supplied observations from an isolated live agent
evaluation. See [eval procedure](evals/README.md),
[validation record](docs/validation.md) and [contribution policies](CONTRIBUTING.md).

## Limitations

APM/OpenAPM and agent interfaces are evolving; compatibility is tested with
the pinned release, not every past/future client. Automatic routing depends on
the model and other installed Skills. Web access, source checkout, history,
build dependencies and a human reviewer are supplied by the contributor.
Backpatch decisions and upstream acceptance remain community decisions.
No tag/release/marketplace publication is performed by local validation.

SemVer applies to behavior as well as paths: during v0.x, breaking changes
require a minor bump and migration notes; patch releases preserve names and
the supported workflow contract. Full policy is in [CONTRIBUTING](CONTRIBUTING.md).
