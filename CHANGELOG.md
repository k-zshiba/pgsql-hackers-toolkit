# Changelog

## 0.1.2 — 2026-10-16

- Clarify versioned `git format-patch` commands, generated filenames and diffstats,
  and `git am` validation against the recorded base.
- Publish GitHub Releases automatically after version-tag validation, with notes
  generated from commits since the previous reachable stable tag.
- Add a repository-only release maintenance Skill for version classification,
  release preparation PRs and explicit publication after human merge.
- Verify that APM preserves the maintenance Skill locally and excludes it from
  archives and consumer deployments; document release scenarios and usage.

## 0.1.1 — 2026-10-12

- Make pgsql-hackers drafts concise while preserving evidence and material details.
- Generate versioned patch attachments with `git format-patch` and real commit
  metadata; package uncommitted changes in an isolated repository.
- Add eval cases for concise drafts and patch packaging.
- Document development on `main` and release preparation through pull requests.

## 0.1.0 — 2026-10-10

- Seven PostgreSQL core Skills with shared evidence and safety instructions.
- APM installation for Codex, Claude Code, GitHub Copilot and portable Agent Skills.
- Package, deployment, integrity and multilingual eval checks.
- PostgreSQL License; no external agent dependencies or vendored source.
