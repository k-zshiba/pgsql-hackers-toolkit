# Consumer examples

Choose a manifest directory for [Codex](codex/apm.yml),
[Claude Code](claude/apm.yml), [both](both/apm.yml), or
[portable Agent Skills](agent-skills/apm.yml). These examples refer to the planned
v0.1.0 Git tag; publish it before using the remote dependency. Before release,
replace the dependency with a local APM path as described in the root README.

Run `apm install` in your consumer workspace; Codex also needs
`apm compile --single-agents`. Set `PG_SOURCE` or provide the checkout path in
the task. Keep PostgreSQL source outside the consumer if you want deployment
artifacts outside patch diffs. Restart/inspect the agent's available Skills.

Portable hosts get Skills without a root context transform: each Skill must
load its linked common contributor contract. A host that cannot follow linked
files is not validated by this example. See [tasks](workflows.md).
