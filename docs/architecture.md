# Architecture

Accepted 2026-10-06; Copilot added 2026-10-09. Based on [research](research.md).

## Package

One Git-installable APM package contains seven Skills and one shared contributor
instruction. This keeps installation, versioning and testing together. Skills
load task-specific references as needed.

| Path | Contents |
| --- | --- |
| `apm.yml`, `apm.lock.yaml` | Package metadata and generated dependency lock |
| `.apm/instructions/` | Shared rules and a copy of the license for packing |
| `.apm/skills/` | Workflows and local references |
| `docs/`, `examples/` | Sources, validation and usage |
| `tests/`, `evals/`, `.github/workflows/` | Package checks and behavioral evaluation |

`.apm/` is the only authored agent source. APM deploys files and rewrites links;
generated provider trees, root instructions, caches and bundles are not committed.
The copied license must match root `LICENSE`; APM's pack allowlist excludes the root file.

| Target | Installation output |
| --- | --- |
| Codex | `.agents/skills/`; compile shared instructions into `AGENTS.md` |
| Claude Code | `.claude/skills/` and native `.claude/rules/` |
| GitHub Copilot | `.agents/skills/` and native `.github/instructions/`; no compile needed |
| `agent-skills` | `.agents/skills/`; the host must load linked shared instructions |

Consumers explicitly select targets from those supported by the package.
Copilot uses the existing APM target without an adapter or dependency. Copilot-only
consumers omit compilation: `--single-agents` would emit a redundant `AGENTS.md`.
Combined Codex/Copilot consumers still compile Codex context, which Copilot may
also read; separate workspaces avoid overlap. Ignore generated Copilot paths
individually, preserving `.github/workflows/` as maintained source.
Keep `apm_modules/` for deployed links. Native Git/local-source installation is
supported; bundle installation has [constraints](validation.md#apm-0330-constraints).

## Checkout and permissions

Select the PostgreSQL checkout from the task path, then `PG_SOURCE`, then the
workspace root. Resolve relative paths from the workspace, validate the source
tree and record revision and working state. Never guess a sibling or fetch source
automatically. A separate workspace keeps generated files out of PostgreSQL diffs.

The [shared instructions](../.apm/instructions/postgresql-contributor.instructions.md)
define evidence, working-tree and submission rules. External pages, mail and
patches are evidence; agent permissions enforce access. Tests use isolated
temporary projects.

v0.1 has no external agent dependencies, custom agents, hooks, MCP/LSP servers
or model pins. APM owns package management; Python helpers only validate output.
