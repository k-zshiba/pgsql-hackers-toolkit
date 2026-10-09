# Architecture decisions for v0.1

Status: accepted, 2026-10-06; Copilot target added 2026-10-09.
Inputs: [research](research.md).

## One APM package

Use Option A: one Git-installable package with seven independently discoverable
Skills. Compared with a meta-package, this gives one install/ref/lock entry,
one release and one integration test surface. Option B would improve selective
installation, but introduces dependency/version coordination and discoverability
costs without a current user need. Separate Skill directories allow a later
split; any dependency restructuring will be treated as a compatibility change.

## Authoring and generated output

`.apm/` is the sole authoring source for agent artifacts. One short, unconditional
instruction owns all shared contributor rules. Skills link to it and add only
their task workflow. APM rewrites package-relative links on deployment.
Intra-Skill references remain self-contained. No empty agents/prompts/hooks
directories, symlink authoring, handwritten AGENTS.md/CLAUDE.md, or provider
configuration is necessary.

The repository's PostgreSQL License notice is also shipped as `.apm/instructions/LICENSE`:
APM 0.33.0's explicit pack allowlist rejects a root `LICENSE` as a non-primitive.
This is a tested byte-identical legal notice, not a second PostgreSQL rule source.
It has no instruction frontmatter and is not loaded as an always-on rule.

APM install deploys Skills/rules; APM compile creates Codex root context.
The package declares Codex, Claude, Copilot and portable Agent Skills compatibility;
APM intersects package restrictions with consumer target selection. Maintainer
validation exercises these four targets and combinations;
**consumers choose their own targets** explicitly. All agents can be tested
from the same source without making any mandatory for consumers.

Copilot uses APM's existing `copilot` target, shared `.agents/skills/` and native
`.github/instructions/*.instructions.md`, with no new Skill, adapter or dependency.
Copilot-only consumers do not compile: 0.33.0's `--single-agents` mode would emit
a redundant `AGENTS.md`. Combined Codex/Copilot consumers still need Codex context,
which Copilot may also read; separate consumers can avoid overlap. Generated
Copilot paths are ignored individually, leaving `.github/workflows/` as source.

Generated roots, provider trees, caches, packed bundles and consumer locks in
scratch projects are not committed. The root lock contains no external
dependencies; frozen install is nevertheless checked. The integration suite
regenerates output and compares content, exercises drift rejection, and checks
links rather than keeping deployed golden copies.

Git source/tag installation is primary. Test default plugin packing for complete
contents and integrity. Direct bundle installation was investigated but is not
a supported consumer route: 0.33.0 does not rewrite our cross-Skill links to
common instructions. Declaring the plugin directory as a dependency resolves
links but drops instruction discovery. Do not add our own deployment layer or
copy shared rules into Skills to hide these upstream limitations. In 0.33.0,
legacy `--format apm` emits an empty bundle for this dependency-free source
package; it is not our distribution path. Direct bundle install also needs
an explicit target flag rather than relying on the consumer manifest.
Do not claim the portable skills-only Agent Plugin format carries instructions.
No registry or marketplace is required; metadata can feed one later.

## Progressive workflows

Seven small Skills correspond to research, design, implementation, test,
review, mail preparation and revision. No subsystem encyclopedia. Each
description states core-development scope and exclusions. Root rules route
work; the applicable Skill loads deeper references only when needed.

Custom agents are deferred: source archaeologist, test strategist and mail
researcher would repeat the Skills. A reviewer with a separate context could
be useful later, but v0.1 does not require parallel work, and current APM
cannot preserve identical tool permission constraints across Codex/Claude.
The review Skill supports author self-review and independent human/agent review
without introducing another maintained persona. No model names are pinned.

## Checkout selection

1. Explicit source path in the task, if given.
2. `PG_SOURCE`, if set (resolve relative values against the consumer cwd).
3. Current repository root, only after identifying a PostgreSQL source tree.

Validate the path using characteristic source files and record Git revision and
working-tree state. Never silently pick a sibling checkout or download source.
Sibling layout is convenient but naming-dependent. An env var is portable but
optional. A custom configuration/checkout resolver is unnecessary; consumer
project detection covers the usual case. The toolkit never vendors PostgreSQL.

A separate consumer workspace plus explicit source path keeps agent deployment
out of PostgreSQL patch diffs. Direct installation in a PostgreSQL checkout is
also supported; review its existing agent files before compilation and keep
toolkit output out of the patch. Neither mode grants destructive Git permission.

## Dependencies and security

Zero external APM/MCP/LSP dependencies or devDependencies. Core workflows are
original local primitives. Do not add scripts/hook execution to consumers.
Python validation uses APM's installed YAML/Markdown libraries; the released
APM CLI is a pinned maintainer tool, not an agent-artifact dependency.
Use the official manifest loader as the current schema compatibility check;
do not reproduce dependency resolution, packing or target deployment.

External evidence is data, never an authority to execute instructions from
patch attachments, emails or retrieved pages. Human approval is required for
posting, sending mail and modifying CommitFest. APM integrity scanning and
harness permissions supplement these prose instructions; prose is not an
enforced sandbox. Tests run with isolated child-process homes in temporary
directories and no global installation.

## Initial repository tree

```text
pgsql-hackers-toolkit/
├── apm.yml                   # package identity, consent, targets
├── apm.lock.yaml             # generated empty dependency closure
├── .apm/
│   ├── instructions/         # one common workflow contract
│   └── skills/               # seven workflows, task-local references
├── docs/                     # research, decisions, validation/self-review
├── tests/                    # structural and isolated APM consumer checks
├── evals/                    # multilingual positive/negative scenarios
├── examples/                 # consumer manifests and task workflows
├── .github/workflows/        # API-key-free validation and artifacts
├── README.md
├── CONTRIBUTING.md           # release/version/dependency policy
├── CHANGELOG.md              # behavior history from the first release
├── .gitignore
└── LICENSE
```

Small fixture validation is the default behavioral gate. A separate grader
accepts real model observations; it does not pretend string matching proves
Skill routing. Live evals remain opt-in with no required service/provider.
