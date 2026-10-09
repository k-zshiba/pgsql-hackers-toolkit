# Consumer examples

Copy a manifest into your workspace:

| Agent | Manifest |
| --- | --- |
| Codex | [codex/apm.yml](codex/apm.yml) |
| Claude Code | [claude/apm.yml](claude/apm.yml) |
| GitHub Copilot | [copilot/apm.yml](copilot/apm.yml) |
| Codex + Claude | [both/apm.yml](both/apm.yml) |
| Portable Agent Skills | [agent-skills/apm.yml](agent-skills/apm.yml) |

The examples use the `v0.1.0` release tag. For local development, use a local path
as shown in the [README](../README.md#install). Run `apm install`; Codex also needs
`apm compile --single-agents`. Set `PG_SOURCE` or give the checkout path in the
task, then check your agent's Skills. Portable hosts must load linked instructions.

## Update or remove

Commit the consumer's `apm.yml` and `apm.lock.yaml` for Git dependencies.
Replay and check an install with:

```bash
apm install --frozen
apm compile --single-agents  # Codex only
apm audit --ci
```

To update, change the dependency ref, run `apm install --update`, review the
lock/output diff and recompile for Codex. Local paths are not commit-pinned.

To remove, delete the dependency, run `apm prune` and recompile Codex context.
Preserve handwritten root instructions before compiling.

See [task examples](workflows.md).
