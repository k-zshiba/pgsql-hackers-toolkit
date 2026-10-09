# Contributing

Keep workflows focused on PostgreSQL core contribution and grounded in current
source and discussion. Repository documentation is in English.

## Edit and test

- Author agent files in `.apm/instructions/` and `.apm/skills/`. Put shared rules
  in the common instruction and task details in Skills or their references.
- Let APM generate provider files and plugin metadata; do not commit generated
  roots, provider trees, caches or bundles. Copilot's `.github/instructions/` and
  `.github/copilot-instructions.md` are generated too; `.github/workflows/` is CI
  source. See [architecture](docs/architecture.md).
- Keep `.apm/instructions/LICENSE` byte-identical to root `LICENSE` so packed
  files carry the legal notice.
- Verify deployed links. Add positive and negative eval cases for behavior changes.
- Discover PostgreSQL revisions, commands, support status and process details
  at task time instead of hard-coding them.

Use Python 3.11+:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python evals/grade.py --validate
```

Tests use temporary projects and isolated child-process homes. See
[validation](docs/validation.md) for coverage and constraints, and
[evals](evals/README.md) for optional live-agent checks. Report checks not run.

To inspect APM output manually, run in an isolated source copy:

```bash
apm install --frozen
apm compile --validate
apm compile --dry-run
apm compile --single-agents
apm audit --ci
apm pack --archive -o dist
```

Generate the root lock with `apm lock` before deployment; do not hand-edit it.

## Version and release

`apm.yml` owns the version. Use `vMAJOR.MINOR.PATCH` Git tags and keep
`CHANGELOG.md` and example dependency refs in sync.

| Change | Version bump |
| --- | --- |
| Compatible wording, links or workflow fixes | Patch |
| New Skill or changed routing contract | Minor, with evals and compatibility notes |
| Breaking names, behavior or installation layout | Minor during v0.x; major after 1.0, with migration notes |

During v0.x, preserve compatibility within each minor line. After 1.0,
compatible additions are minor releases.

1. Recheck official docs when changing deployment or upgrading APM; update version,
   changelog and examples.
2. Run tests and eval validation; review the final diff, archive contents and links.
3. Prepare the immutable tag and release description. Obtain explicit authorization
   before pushing tags, uploading assets or publishing to a marketplace.
4. Test the published tag from a fresh consumer and replay its committed lock with
   a cold `apm install --frozen`. Local fixtures cannot prove public availability.

## Dependencies and review

v0.1 has no external agent dependencies. Add an adapter, agent or helper only
for a concrete need. Before adding a dependency, record its source/ref, resolved
commit/hash, license obligations, maintenance plan, transitive dependencies,
permissions and network/credential requirements. Keep optional dependencies
from becoming essential to core workflows.

Declare dependencies in `apm.yml`, generate the lock through APM and verify frozen
install plus audit. Keep dev-only artifacts out of shipped files. Review upstream
licenses, advisories and dependency changes on upgrades; `requirements-dev.txt`
pins APM, while its Python dependencies are not locked by `apm.lock.yaml`.

Review scope, evidence, open questions, preservation of user work, external-write
authorization, test claims, Skill boundaries, evals and packaging. Toolkit changes
use this repository's review process; PostgreSQL patches follow pgsql-hackers
and CommitFest.
