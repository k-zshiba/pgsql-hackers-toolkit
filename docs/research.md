# Research sources

Research date: 2026-10-06 (Asia/Tokyo). These sources informed the package design;
recheck them when upgrading. Workflow text is original; reference-project content
is not imported.

## APM

Tested release: [0.33.0](https://github.com/microsoft/apm/releases/tag/v0.33.0).
Inspected source: `18c4c43c924ceae890fe0f2038806690e5b2d6c8`.

| Topic | Finding and source |
| --- | --- |
| Package | Git-installable `apm.yml` with canonical `.apm/` primitives. [Anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/) |
| Manifest/schema | Use `targets`, explicit packing `includes` and the supported OpenAPM 0.1.41 identity; validate through the CLI loader. [Manifest](https://microsoft.github.io/apm/reference/manifest-schema/), [draft specification](https://microsoft.github.io/apm/specs/openapm-v01/) |
| Primitives | Skills use Agent Skills frontmatter; shared instructions compile for Codex and deploy as native Claude/Copilot rules. [Skills](https://microsoft.github.io/apm/producer/author-primitives/skills/), [instructions/agents](https://microsoft.github.io/apm/producer/author-primitives/instructions-and-agents/) |
| Install/lock | Git refs and local paths are supported; frozen install checks lock agreement, audit checks deployed content. [Install](https://microsoft.github.io/apm/consumer/install-packages/), [lockfile](https://microsoft.github.io/apm/reference/lockfile-spec/) |
| Targets/links | Consumer selection intersects package targets; deployed links can depend on `apm_modules/`. [Targets](https://microsoft.github.io/apm/reference/targets-matrix/), [relative links](https://microsoft.github.io/apm/producer/package-relative-links/) |
| Verify/pack | Compile validates and generates context; default pack creates plugin artifacts. Installation constraints are in [validation](validation.md#apm-0330-constraints). [Verify loop](https://microsoft.github.io/apm/producer/preview-and-validate/), [pack](https://microsoft.github.io/apm/producer/pack-a-bundle/) |
| Security | Unicode scans and integrity checks supplement agent permissions. [Security](https://microsoft.github.io/apm/enterprise/security/), [policy](https://microsoft.github.io/apm/enterprise/policy-reference/) |

APM owns deployment and package management. Custom agents, prompts, hooks and
marketplace infrastructure were unnecessary for v0.1.

## PostgreSQL

Inspected the [official repository](https://git.postgresql.org/gitweb/?p=postgresql.git)
through its [mirror](https://github.com/postgres/postgres) at
`dfcf6fa7749d1fc4660d03590f14dca7c855048c`. Consumers use their actual checkout.

- Process: [developer entrypoint](https://www.postgresql.org/developer/),
  [FAQ](https://wiki.postgresql.org/wiki/Developer_FAQ),
  [submitting](https://wiki.postgresql.org/wiki/Submitting_a_Patch),
  [reviewing](https://wiki.postgresql.org/wiki/Reviewing_a_Patch) and
  [CommitFest](https://commitfest.postgresql.org/).
- Style: [coding conventions](https://www.postgresql.org/docs/devel/source.html)
  and [pgindent README](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/src/tools/pgindent/README).
- Tests: [test README](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/src/test/README),
  [TAP](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/src/test/perl/README),
  [isolation](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/src/test/isolation/README),
  [regression Makefile](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/src/test/regress/GNUmakefile)
  and [Meson source](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/meson.build).

Source and local READMEs determine commands and conventions. Wiki and online devel
docs can lag; verify current process, branch status and subsystem behavior.

Discussion examples informed the research/revision workflows:
[row pattern recognition](https://www.postgresql.org/message-id/CAAAe_zCsaf=WedELLjqLe3BV_8dWiO1DPDGA9sXj4qhe%2B=-XXw@mail.gmail.com),
[JIT fix](https://www.postgresql.org/message-id/flat/CAAAe_zD6jGANGZFKnHLKHF8izqmqqJbVe=NOuERFwN_Spj5VOA@mail.gmail.com)
([CF 6870](https://commitfest.postgresql.org/patch/6870/)) and
[slotsync backpatch](https://www.postgresql.org/message-id/CAHGQGwH_AAbtsiYDJt65N7_4PJ0CgOJmBEaCq68e5_tcuG_vXw@mail.gmail.com).
Read whole threads and verify versions, prerequisites and branch-specific risks.

## GitHub Copilot follow-up — 2026-10-09

Rechecked the official [latest APM release](https://github.com/microsoft/apm/releases/latest):
0.33.0 remains the observed release. Its existing `copilot` target needs no
toolchain upgrade. [GitHub Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
and [VS Code Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
confirm support for APM's shared `.agents/skills/` path.
[Copilot CLI instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)
support `.github/instructions/` with `applyTo`; the APM installation probe preserves
our `"**"` rule. [Copilot CLI Skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
documents discovery and reload commands. See [architecture](architecture.md) for
the compile decision and [validation](validation.md) for tested scope and limits.

## Agent formats and reference projects

Official formats:
[Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Codex Skills](https://learn.chatgpt.com/docs/build-skills),
[Claude Skills](https://code.claude.com/docs/en/skills),
[Claude rules](https://code.claude.com/docs/en/memory) and the
[Agent Skills specification](https://agentskills.io/specification).
Deployment checks establish paths and content; live behavior needs separate evals.

| Reference project | Design input |
| --- | --- |
| [postgres-claude](https://github.com/matejformanek/postgres-claude) | Core scope, citations and isolated workspaces; avoid a static internals corpus |
| [postgres-skills](https://github.com/microsoft/postgres-skills) | Intent routing; application/cloud workflows are outside this package |
| [PostGIS AGENTS.md](https://github.com/postgis/postgis/blob/master/AGENTS.md) | Small navigation entrypoint; extension tooling differs from core |
| [APM](https://github.com/microsoft/apm) | Native primitives and deployment; multi-package scheduling exceeds current needs |

The original toolkit uses the [PostgreSQL License](../LICENSE), with toolkit
contributors as copyright holders. See the [official license](https://www.postgresql.org/about/licence/)
and [SPDX reference](https://spdx.org/licenses/PostgreSQL.html).
