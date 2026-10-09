# Behavioral evaluation

[scenarios.json](scenarios.json) covers seven workflows, English/Japanese prompts,
application/operations negatives and safety cases. Default CI validates fixtures
and the grader; live routing requires agent observations.

## Collect observations

1. Install the package in an isolated workspace using the [README](../README.md#install).
2. Start a fresh agent session per scenario with its prompt, discovered Skill
   metadata and common instructions. Request an initial plan; hide expected
   Skills and the rubric. Use no live database or external writes.
3. Record client version, package commit, model, settings and transcript.
4. Have a human reviewer map the trace to criteria in [grade.py](grade.py).
   Record successful and forbidden behavior in `observed`.

These scenarios test routing and initial planning. Testing patch execution
requires separate source, patches, tests and review of outcomes. A safe plan can
satisfy planning criteria; missing evidence must not be fabricated.

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
