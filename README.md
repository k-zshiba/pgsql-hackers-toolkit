# pgsql-hackers-toolkit

AI agent Skills for PostgreSQL core development: research, design, implement,
test, review, revise patches and draft pgsql-hackers mail.

Supports Codex, Claude Code and portable Agent Skills through
[Agent Package Manager (APM)](https://github.com/microsoft/apm).
Application SQL, query tuning and database administration are outside its scope.

## Install

Use Python 3.11+ and the tested APM version:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install apm-cli==0.33.0
```

Clone this repository beside a separate workspace. In that workspace, create
`apm.yml`:

```yaml
name: my-postgresql-workspace
version: 0.1.0
targets: [codex]  # or [claude], [codex, claude], [agent-skills]
dependencies:
  apm:
    - ../pgsql-hackers-toolkit
```

Run in the workspace:

```bash
apm install
apm compile --single-agents  # Codex only
export PG_SOURCE=/absolute/path/to/postgresql
```

The `v0.1.0` release is unpublished. After publication, replace the local path
with `k-zshiba/pgsql-hackers-toolkit#v0.1.0` for a Git install.
Use source packages; packed ZIP installation has
[known limitations](docs/validation.md#apm-0330-constraints).

For existing workspaces, inspect `apm compile --dry-run` and preserve handwritten
agent instructions before compiling. Keep generated files out of PostgreSQL patches
and keep `apm_modules/` available for linked instructions.

## Use

Start or restart your agent in the workspace and check its available Skills.
Provide a PostgreSQL checkout path in the task or set `PG_SOURCE`; otherwise,
the workspace root must be a PostgreSQL source tree. Relative `PG_SOURCE` paths
resolve from the workspace. Configure agent access to that checkout as needed.

For example:

```text
Investigate this planner bug in PG_SOURCE. Check source, callers, tests and
pgsql-hackers history. Explain the evidence and unknowns before editing.
```

| Skill | Purpose |
| --- | --- |
| [research-postgresql](.apm/skills/research-postgresql/SKILL.md) | Investigate source, history, discussions and backpatch suitability |
| [design-pg-patch](.apm/skills/design-pg-patch/SKILL.md) | Define behavior, scope and tests |
| [implement-pg-patch](.apm/skills/implement-pg-patch/SKILL.md) | Implement a scoped change with docs and tests |
| [test-pg-patch](.apm/skills/test-pg-patch/SKILL.md) | Run validation appropriate to the checkout |
| [review-pg-patch](.apm/skills/review-pg-patch/SKILL.md) | Review correctness, compatibility and coverage |
| [revise-pg-patch](.apm/skills/revise-pg-patch/SKILL.md) | Address feedback and retest |
| [prepare-pgsql-hackers-post](.apm/skills/prepare-pgsql-hackers-post/SKILL.md) | Draft proposals, submissions, reviews and replies |

Use `$research-postgresql` in Codex or `/research-postgresql` in Claude to invoke
research explicitly. See [task examples](examples/workflows.md).

The [shared instructions](.apm/instructions/postgresql-contributor.instructions.md)
require current evidence, preservation of user changes and honest test results.
Mail and CommitFest updates require explicit authorization. Agent permissions
remain responsible for enforcing access; automatic Skill routing needs live evaluation.

## Documentation

- [Consumer examples and updates](examples/README.md)
- [Development, tests and releases](CONTRIBUTING.md)
- [Package structure](docs/architecture.md)
- [Research sources](docs/research.md)
- [Validation and limitations](docs/validation.md)
- [Behavioral evaluation](evals/README.md)
- [Changelog](CHANGELOG.md)

Licensed under the [PostgreSQL License](LICENSE).
