---
name: release-pgsql-hackers-toolkit
description: Prepare a release PR or publish a merged release of k-zshiba/pgsql-hackers-toolkit, including version classification, validation, tags and GitHub Release verification. Use only for maintaining this repository, not for PostgreSQL server releases or consumer projects.
---

# Release pgsql-hackers-toolkit

Read [CONTRIBUTING.md](../../../CONTRIBUTING.md#version-and-release) and the
[release workflow](../../../.github/workflows/validate.yml) at the target revision.
This is a repository maintenance Skill; it is not part of the seven distributed
PostgreSQL development Skills.

## Establish the repository and stage

- Resolve the requested checkout, record its absolute root, HEAD, branch and
  `git status --short`, and verify the manifest name and GitHub remote identify
  `k-zshiba/pgsql-hackers-toolkit`. Do not run release operations in a consumer
  or PostgreSQL source tree. Verify `gh` authentication and repository access;
  scope GitHub commands to this repository with `--repo`.
- Distinguish preparation (including an unqualified "prepare a release" or
  "リリースして") from an explicit request to publish a merged release. Preparation
  ends with a PR; it never merges, tags or publishes. An explicit publication
  request authorizes the tag push and its automatic GitHub Release publication;
  do not ask again when that authorization is already present. Loading this
  Skill authorizes no publication. For version advice alone, stop after change
  classification without editing files, pushing a branch or opening a PR.
- Fetch `origin` main and tags without force. If network access fails, report
  that freshness is unknown and stop before a release PR or tag push. Preserve
  tracked and untracked work; use a separate worktree for release preparation
  and inspection rather than switching or cleaning the user's working tree.

## Classify changes

- For preparation, compare refreshed `origin/main` with its highest numeric
  reachable `vMAJOR.MINOR.PATCH` tag (no leading zeros or prereleases), using
  numeric ordering as in [release_notes.py](../../../.github/scripts/release_notes.py).
  Verify that tag has a published, non-draft, non-prerelease GitHub Release.
  If it represents an incomplete publication, report it and stop preparation;
  recovering publication requires an explicit publication request.
  If there is no prior release, ask for the initial version.
- Read the actual diff, relevant files and commit history across the whole range.
  Explain the compatibility impact and cite changed paths. Commit subjects alone
  do not establish compatibility. Select the largest required bump:

  | Change | Bump |
  | --- | --- |
  | Compatible wording, links or workflow fixes | Patch |
  | New distributed Skill or changed routing contract | Minor |
  | Breaking names, behavior or installation layout | Minor in v0.x; major after 1.0 |

- A repository-only maintenance Skill is not a new distributed Skill. Assess
  its actual impact; its addition alone does not require a minor bump. Do not
  automatically graduate v0.x to 1.0. If compatibility is unclear, ask about
  the specific unresolved behavior before choosing a version. Explain any
  conflict with a requested version instead of silently overriding the policy.
- Report base tag, target SHA, change classification, proposed next version and
  migration/compatibility notes. Do not create an empty release if there are no
  changes. On a retry, inspect existing release PRs before preparing duplicates.

## Prepare a release PR

1. Create a dedicated `release/vMAJOR.MINOR.PATCH` branch in an isolated worktree
   from refreshed `origin/main`; reuse an existing matching preparation safely.
   Update `apm.yml`, a dated `CHANGELOG.md` entry, and all `examples/*/apm.yml`
   dependency refs together. Generate locks with APM only if actually required.
2. Follow the current contributor checks: `python -m unittest discover -s tests -v`
   and `python evals/grade.py --validate` with the pinned development dependencies.
   In an isolated source copy, run frozen install, compile validation and dry-run,
   single-AGENTS compilation, audit and archive packing as documented. Review
   archive contents and links, including exclusion of this maintenance Skill.
   Record commands, results and coverage limits; fix failures before proceeding.
3. Review the final release diff, commit only preparation files, push only the
   preparation branch, and use `gh pr create --base main` (or update the matching
   PR). Include base/target, version reasoning, compatibility notes and validation;
   supply multiline bodies via a file. Report its URL and stop for human merge.

## Publish a merged release

1. Identify the requested version and release PR. Check with `gh pr view` that
   it is merged into `main`; resolve its merge commit and verify that commit is
   reachable from refreshed `origin/main`. Inspect version, changelog, example
   refs and release workflow at that exact commit, even if main has advanced.
   Verify successful required CI for that SHA, not just the pre-merge PR head.
   Do not substitute current HEAD or another commit when evidence is missing.
2. Check local and remote tags and any existing GitHub Release. Existing tags
   must peel to the verified merge SHA; verify a Release uses that remote tag
   and is published as a stable release. Report conflicting SHAs or publication
   states without overwriting or deleting them. Reuse matching completed work.
3. If absent, create an annotated tag on the verified SHA with
   `git tag -a "$tag" "$sha" -m "Release $tag"`. Push only that ref using
   `git push origin "refs/tags/$tag:refs/tags/$tag"`; never force or push all tags.
   A matching remote tag needs no new push.
4. Find the tag-push run of the existing validation/release workflow for that
   tag and SHA, wait for completion and verify the resulting Release URL, title,
   stable publication state and notes. Use the existing CI publisher rather than
   a second `gh release create` path. For a transient failure, inspect logs and
   rerun the matching workflow once; stop and report persistent failures. If
   publication succeeds but consumer verification fails, report the published
   state rather than attempting to delete or retag it.
5. In a fresh temporary consumer and isolated APM state, install this repository
   pinned to the published tag, verify the generated lock resolves to the tagged
   SHA, remove only that consumer's disposable module/cache state, and replay its
   committed lock with a cold `apm install --frozen`. Check the seven distributed
   Skills and their links; the maintenance Skill must not be deployed. Follow
   [consumer validation](../../../docs/validation.md) for current constraints.
6. Report version, merge/tag SHA, PR and Release URLs, workflow result and public
   consumer verification, explicitly identifying any incomplete checks. Asset
   uploads and marketplace publication need a separate request.
