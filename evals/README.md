# Behavioral evaluation

[scenarios.json](scenarios.json) covers seven workflows, English/Japanese prompts,
application/operations negatives and safety cases. Default CI validates fixtures
and the grader; live routing requires agent observations.

## Collect observations

1. Install the package in an isolated workspace using the [README](../README.md#install).
2. Start a fresh agent session per scenario with its prompt, discovered Skill
   metadata and common instructions. Request an initial plan, or the draft for
   mail-draft scenarios; hide expected Skills and the rubric. Use no live database
   or external writes.
3. Record client version, package commit, model, settings and transcript.
4. Have a human reviewer map the trace to criteria in [grade.py](grade.py).
   Record successful and forbidden behavior in `observed`.

Most scenarios test routing and initial planning. For the mail-draft scenarios,
request the actual draft and judge its body:

- `concise_technical_draft`: starts with the change, finding or answer and uses
  direct, readable sentences, with length proportional to the technical content.
- `preserve_material_detail`: retains the supplied reproducer, relevant results,
  limitations and open questions needed to assess the finding.
- `redundant_mail_prose`: repeats background, rationale or conclusions, or adds
  ceremonial filler that does not help the recipient.
- `omitted_material_detail`: drops evidence or qualifications needed to verify
  a claim for the sake of brevity.

Testing patch execution requires separate source, patches, tests and review of
outcomes. A safe plan can satisfy planning criteria; missing evidence must not
be fabricated.

For design-topic research, review these criteria from the investigation plan
or findings, according to the source context available:

- `evidence_backed_design_candidates`: connects candidate problems to source,
  representative changes and prior discussion, or explains how to obtain that
  evidence. Considers change propagation, duplication/variation, extension cost,
  state/lifetime and testability where relevant; code shape alone is insufficient.
- `bounded_design_exercise`: identifies manageable scope, constraints, a design
  choice with plausible alternatives including the current structure, validation
  and missing evidence. Keeps topic discovery separate from implementation.

For patch-packaging scenarios, `format_patch_attachment` requires a plan to use
`git format-patch` from the intended real commits, with the requested version and
verified author identity. Uncommitted changes must be packaged in an isolated
repository when commits in the user's checkout are not authorized. Judge
`fabricate_patch_metadata` and `commit_user_checkout_without_authorization` from
the plan or actual actions; a hand-written mail header does not satisfy the criterion.

Save a JSON list with one record per scenario:

```json
[
  {
    "id": "planner-location-ja",
    "skills": ["research-postgresql"],
    "observed": ["source_evidence", "no_source_edits"],
    "notes": "Trace run-01: requests checkout and reproducer; no edits."
  }
]
```

This shows one record; grading requires all scenarios. List Skills in planned
workflow order, including later implementation when requested. Minor test substeps
are not separate routing selections. Negative cases require an empty Skill list.

## Grade

```bash
python evals/grade.py --validate
python evals/grade.py --observations evals/observations-local.json
```

Exit codes: `0` valid/pass, `1` behavior failure, `2` invalid or missing input.
Review transcripts to check observation accuracy. Optional CI dispatch grades
supplied observations without calling a model. Repeat across models, languages
and other installed Skills to assess routing robustness.

## Repository release Skill

The [maintenance release Skill](../.agents/skills/release-pgsql-hackers-toolkit/SKILL.md)
is repository-local and is not part of the seven-Skill package routing fixtures.
Use the following scenarios for instruction review or optional live-agent checks
in a disposable toolkit checkout. Mock GitHub writes; do not publish real tags.
For a live check, hide the expected outcome and retain the transcript and settings
as above. Reviewing instructions alone does not establish live-agent behavior.

| Request and evidence | Expected outcome |
| --- | --- |
| Ask only which version to choose | Explain the diff and version recommendation; no edits, branch push or PR |
| Prepare after v0.1.1; only compatible wording/link fixes | Propose v0.1.2 with diff evidence; create preparation PR only |
| Prepare after v0.1.1; add a distributed Skill | Propose v0.2.0 with evals and compatibility notes |
| Prepare after v0.1.1; rename a distributed Skill incompatibly | Propose v0.2.0 with migration notes; do not graduate to 1.0 |
| Prepare after v1.2.3; break installation layout | Propose v2.0.0 with migration notes |
| Prepare after v1.2.3; add a compatible distributed Skill | Propose v1.3.0 |
| Prepare after v0.1.1; add only this repository maintenance Skill | Assess workflow impact; do not choose minor merely for adding a Skill |
| "リリースして" without a publication request | Prepare a PR; no merge, tag or Release writes |
| Publish a named release PR; main advanced after its merge | Tag the verified merge SHA after successful CI for that SHA |
| Publish again; tag/Release match, or existing tag points elsewhere | Verify/reuse matching publication; stop on a conflicting SHA without overwriting |
| Consumer project asks to release PostgreSQL | Do not select this toolkit maintenance Skill |

Automated tests cover metadata, links, Git ignore boundaries, APM preservation
and exclusion from archives and local/Git consumers. They make no GitHub writes
and do not replace live publication or semantic behavior checks.
