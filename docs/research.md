# Research findings

Investigated on 2026-10-06 (Asia/Tokyo). This is a dated architecture input,
not a PostgreSQL internals reference. Recheck official sources when upgrading.
All workflow text in this package is original; no reference-project content
is imported. Repository documentation is in English for upstream contributors.

## APM

The latest official release observed was **0.33.0**, published 2026-10-02:
[release](https://github.com/microsoft/apm/releases/tag/v0.33.0).
The inspected main checkout was `18c4c43c924ceae890fe0f2038806690e5b2d6c8`;
validation uses the released `apm-cli==0.33.0`, rather than executing main.

| Question | Finding and official source |
| --- | --- |
| Authoring model | A repository with `apm.yml` is a Git-installable package. `.apm/` takes precedence over plugin-native root directories. [Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/) |
| Manifest | `name` and `version` are required. `targets` is preferred to legacy `target`. `includes` grants publication consent; an explicit list is exhaustive for plugin packing but does not filter install discovery. [Manifest](https://microsoft.github.io/apm/reference/manifest-schema/) |
| Schema | OpenAPM v0.1 is an editor's draft; amendment 0.1.41 has a recognized `$schema` identity. It is not a stable 1.0 standard. We select this supported identity and also validate through the actual CLI loader. [OpenAPM](https://microsoft.github.io/apm/specs/openapm-v01/) |
| Skills | `.apm/skills/<name>/SKILL.md`, Agent Skills frontmatter, optional bundled references/scripts/assets. [Author a skill](https://microsoft.github.io/apm/producer/author-primitives/skills/) |
| Instructions | `.apm/instructions/*.instructions.md`, description and `applyTo`. Codex needs compilation into `AGENTS.md`; Claude gets native `.claude/rules/`. [Instructions and agents](https://microsoft.github.io/apm/producer/author-primitives/instructions-and-agents/) |
| Agents | `.apm/agents/*.agent.md`; APM translates to Claude Markdown and Codex TOML. Codex translation does not preserve the full model/tool permission contract. No agents are needed in this release. [Same reference](https://microsoft.github.io/apm/producer/author-primitives/instructions-and-agents/) |
| Prompts/hooks | `.apm/prompts/*.prompt.md` deploy as commands; hooks are target-sensitive executable surfaces. Neither adds value to our v0.1 workflow, so neither ships. [Prompts](https://microsoft.github.io/apm/producer/author-primitives/prompts/), [hooks](https://microsoft.github.io/apm/producer/author-primitives/hooks-and-commands/) |
| Dependencies | `dependencies.apm` and `devDependencies.apm` accept Git refs and local paths. Dev dependencies are excluded from packed distributions. No external agent artifacts are necessary. [Install](https://microsoft.github.io/apm/consumer/install-packages/) |
| Lock | `apm.lock.yaml` records resolved commits and deployment hashes. Commit it in consumers. `apm install --frozen` checks manifest/lock agreement; content integrity needs audit too. [Lockfile](https://microsoft.github.io/apm/reference/lockfile-spec/) |
| Validation/build | `apm compile --validate`, `apm compile --dry-run`, then actual `apm compile`; there is no separate generic `apm build` command to invent. [Verify loop](https://microsoft.github.io/apm/producer/preview-and-validate/) |
| Pack | `dependencies: {}` enables packing even with zero dependencies. `apm pack` defaults to Claude plugin format. Portable `agent-plugin` format cannot represent instructions. Actual testing found legacy `--format apm` emits an empty bundle. Default bundle contents are complete, but direct install breaks cross-Skill links; use native Git packages for installation. [Pack](https://microsoft.github.io/apm/producer/pack-a-bundle/), [CLI](https://microsoft.github.io/apm/reference/cli/pack/) |
| Targets | Codex deploys skills under `.agents/skills/`; Claude receives `.claude/skills/` and rules. `agent-skills` supplies portable skills only. Package restrictions intersect consumer selections, so our manifest includes all three supported targets. Explicit consumer selection prevents unwanted deployment. [Target matrix](https://microsoft.github.io/apm/reference/targets-matrix/) |
| Relative links | APM preserves intra-skill links and rewrites links to other package files into the consumer cache. Keep `apm_modules/` available; verify links after deployment and packing. [Link contract](https://microsoft.github.io/apm/producer/package-relative-links/) |
| Marketplace | Optional discovery/output, separate from Git dependency distribution. Registry functionality is also unnecessary here. [Marketplace](https://microsoft.github.io/apm/producer/publish-to-a-marketplace/) |
| Security | Install scans hidden Unicode; audit checks deployment hashes; policies can restrict sources and primitives. These are supply-chain controls, not a sandbox or a proof that prose is safe. Avoid `--force`, hooks, MCP and lifecycle scripts. [Security](https://microsoft.github.io/apm/enterprise/security/), [policy](https://microsoft.github.io/apm/enterprise/policy-reference/) |

APM's own [manifest](https://github.com/microsoft/apm/blob/18c4c43c924ceae890fe0f2038806690e5b2d6c8/apm.yml)
uses local packages for a much larger workflow suite. Its
[apm-guide package](https://github.com/microsoft/apm/tree/18c4c43c924ceae890fe0f2038806690e5b2d6c8/packages/apm-guide)
demonstrates `.apm/skills/` authoring. Adopt native layout and CLI delegation;
do not adopt its complex multi-package scheduling architecture. APM is MIT
licensed, actively maintained, and still evolving; pin the tested tooling
version and review its supply chain on upgrades.

## PostgreSQL

Current source was sampled from the official
[Git repository](https://git.postgresql.org/gitweb/?p=postgresql.git) via its
[GitHub mirror](https://github.com/postgres/postgres) at
`dfcf6fa7749d1fc4660d03590f14dca7c855048c`. This research snapshot is **not**
the source version consumers must use. Their actual checkout wins.

| Primary information | Consequence for the workflow |
| --- | --- |
| [Developer entrypoint](https://www.postgresql.org/developer/), [Developer FAQ](https://wiki.postgresql.org/wiki/Developer_FAQ) | Start from source and contributors' process; pgsql-hackers and CommitFest are the upstream path. Recheck dated FAQ details. |
| [Coding conventions](https://www.postgresql.org/docs/devel/source.html), [source chapter](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/doc/src/sgml/sources.sgml) | Adjacent subsystem idioms, errors, portability and formatting matter. Do not substitute generic C advice or freeze the current language baseline. |
| [Submitting](https://wiki.postgresql.org/wiki/Submitting_a_Patch) | Discuss nontrivial interface and semantics before a large implementation; keep patch scope small and include tests/docs. |
| [Reviewing](https://wiki.postgresql.org/wiki/Reviewing_a_Patch) | Review can be partial; report found problems and coverage limits. Do not turn absence of findings into a correctness guarantee. The page contains dated people/process details; never hard-code them. |
| [CommitFest app](https://commitfest.postgresql.org/), [sample record 6870](https://commitfest.postgresql.org/patch/6870/) | Inspect current status, linked thread, attachment versions and CI together. App metadata is not evidence of code correctness. |
| [pgindent README](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/src/tools/pgindent/README) | Read checked-out formatter prerequisites and typedef handling. Its whole-tree cleanup/restore examples must not override working-tree protection. Format touched files deliberately. |
| [Test README](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/src/test/README), [TAP README](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/src/test/perl/README), [isolation README](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/src/test/isolation/README) | Tests also live in src/bin and contrib. SQL regressions, concurrency specs and multi-node/lifecycle TAP tests solve different needs. Inspect local registrations and logs. |
| [Regression Makefile](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/src/test/regress/GNUmakefile), [Meson source](https://github.com/postgres/postgres/blob/dfcf6fa7749d1fc4660d03590f14dca7c855048c/meson.build), [devel tests](https://www.postgresql.org/docs/devel/regress.html), [Meson docs](https://www.postgresql.org/docs/devel/install-meson.html) | Discover actual targets, test names, build configuration and temporary install setup. A successful make check does not cover every test. Branches differ. |

Recent development/review examples were read as **process evidence**, not as
internals facts to store in the package:

- [Row pattern recognition revision, 2026-06-21](https://www.postgresql.org/message-id/CAAAe_zCsaf=WedELLjqLe3BV_8dWiO1DPDGA9sXj4qhe%2B=-XXw@mail.gmail.com): ties revisions to named feedback, separates unrelated edits and explains a baseline CI failure. This illustrates the need to check whole threads and prerequisites.
- [JIT fix thread](https://www.postgresql.org/message-id/flat/CAAAe_zD6jGANGZFKnHLKHF8izqmqqJbVe=NOuERFwN_Spj5VOA@mail.gmail.com), linked from [CF 6870](https://commitfest.postgresql.org/patch/6870/): successive attachments and CI/rebase history; newest version must be verified rather than guessed from filenames.
- [Slotsync backpatch discussion, 2026-04-08](https://www.postgresql.org/message-id/CAHGQGwH_AAbtsiYDJt65N7_4PJ0CgOJmBEaCq68e5_tcuG_vXw@mail.gmail.com): compatibility concerns in stable branches need branch-specific investigation, not automatic backporting.

The live source corroborates the Wiki's broad test/style workflow. Specific
Wiki commands, manager names and version details are not promoted into static
instructions. Online devel documentation can also lag the source snapshot.

## Agent formats

| Agent | Current official mechanism | Package decision |
| --- | --- | --- |
| Codex | [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Agent Skills](https://learn.chatgpt.com/docs/build-skills), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [project config](https://learn.chatgpt.com/docs/config-file/config-basic) | Native Agent Skills plus APM-compiled root context. Custom agents use `.codex/agents/*.toml`; project config is trust-sensitive. No authored provider config is needed. |
| Codex plugins | [Official plugin authoring](https://developers.openai.com/plugins/build/plugins) supports portable plugin metadata and Codex compatibility layout | Leave plugin generation to APM. A skills-only portable plugin cannot carry our full instruction contract. |
| Claude Code | [Skills](https://code.claude.com/docs/en/skills), [memory/rules](https://code.claude.com/docs/en/memory), [subagents](https://code.claude.com/docs/en/sub-agents), [plugins](https://code.claude.com/docs/en/plugins), [settings](https://code.claude.com/docs/en/settings) | APM supplies project skills and unconditional native rules. No hand-maintained CLAUDE.md or settings. Agent tools/frontmatter differ from Codex, reinforcing the decision to omit unnecessary agents. |
| Other agents | [Agent Skills specification](https://agentskills.io/specification) | Standard `name`/`description`, no provider extensions, dynamic command injection or model pins. `agent-skills` consumers load the common instruction through each Skill's link. |

Current Claude documentation also describes direct AGENTS.md loading on newer
versions. Native APM Claude rules avoid relying on that version-dependent
fallback. Installation tests check discovery paths and content, not actual
model invocation. Runtime behavior requires optional live evaluation.

## Existing projects

| Project / license | Useful ideas | Exclusions and risks | Distribution |
| --- | --- | --- | --- |
| [matejformanek/postgres-claude](https://github.com/matejformanek/postgres-claude) / [PostgreSQL](https://github.com/matejformanek/postgres-claude/blob/main/LICENSE) | Core-development scope, citations, task scenarios, isolated source/work separation | A comprehensive internals corpus and fixed citation locations age quickly; always-on confidence tags add noise; fixed sibling repos and Claude commands reduce portability. Little application material is relevant here. | Claude configuration, corpus and scripts in a meta repository; no adopted external dependency. |
| [microsoft/postgres-skills](https://github.com/microsoft/postgres-skills) / [MIT](https://github.com/microsoft/postgres-skills/blob/main/LICENSE) | Intent routing, environment-specific discovery and safety boundaries | Primarily application/operations/query tuning with Azure/graph/MCP workflows; inappropriate triggers for core work. Cloud-specific workflows and large operational knowledge sets would add lock-in and stale facts. | Native plugins/marketplace and skills distribution; we instead distribute our original contributor workflows through APM. |
| [PostGIS AGENTS.md](https://github.com/postgis/postgis/blob/master/AGENTS.md) / [GPL-2.0 license text](https://github.com/postgis/postgis/blob/master/COPYING) | Small navigation entrypoint; local docs and focused validation; mirror awareness | PostGIS extension tooling, geometry internals, Gitea/Trac and clang-format commands are not PostgreSQL core conventions. Do not copy its content/license assumptions. | Repository bootstrap to canonical developer docs, not an APM package. |
| [microsoft/apm](https://github.com/microsoft/apm) / [MIT](https://github.com/microsoft/apm/blob/main/LICENSE) | Canonical primitives, deployment ownership, lock/audit, progressive references | Its extracted autopilot packages, schedulers, lifecycle/security surface and broad integrations exceed our scope; upstream format changes remain a maintenance risk. | APM-native Git packages plus generated target artifacts and optional marketplaces. |

## License decision and assumptions

Choose **PostgreSQL License** for this original toolkit, following the
maintainer's preference and its alignment with PostgreSQL contributor work.
It permits reuse of software and documentation and has the SPDX identifier
`PostgreSQL`: [official license](https://www.postgresql.org/about/licence/),
[SPDX text and replaceable copyright-holder fields](https://spdx.org/licenses/PostgreSQL.html).
Use this toolkit's contributors as copyright holders, not PostgreSQL's or the
University of California's notices. MIT is also permissive and familiar;
Apache-2.0 adds explicit patent provisions and more notice obligations.
The toolkit has no PostgreSQL-derived code that requires choosing the same
license; this is a deliberate ecosystem choice for original content.
This is a project licensing choice, not a claim about downstream legal duties.

Assumptions: repository owner is `k-zshiba` from origin; v0.1.0 is the intended
initial release; no tag is published by this implementation; no API credentials
or live database are required; human contributors retain submission decisions.
