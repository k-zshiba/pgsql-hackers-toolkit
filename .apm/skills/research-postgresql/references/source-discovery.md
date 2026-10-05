# Source discovery

Start in the selected PostgreSQL checkout; these commands are read-only
examples, with the path/symbol replaced from the task:

```bash
git -C "$PG_SOURCE" rev-parse HEAD
git -C "$PG_SOURCE" status --short
rg -n 'symbol_or_error_text' "$PG_SOURCE/src"
git -C "$PG_SOURCE" log --oneline -- path/to/file.c
git -C "$PG_SOURCE" blame -L 100,160 -- path/to/file.c
git -C "$PG_SOURCE" show <commit> -- path/to/file.c
```

Do not assume `PG_SOURCE` is set; the common contract also allows an explicit
path or the validated consumer repository. Line ranges are discovery aids:
read the whole function and follow boundary conditions. Use `rg --files` to
find README files and tests near the discovered code. Do not memorize a
subsystem-to-path map; names and implementations change.

Primary online starting points:

- [Official source browser](https://git.postgresql.org/gitweb/?p=postgresql.git)
  and [official Git mirror](https://github.com/postgres/postgres).
- [Developer entrypoint](https://www.postgresql.org/developer/) and
  [development documentation](https://www.postgresql.org/docs/devel/).
- [pgsql-hackers archive](https://www.postgresql.org/list/pgsql-hackers/).
- [CommitFest application](https://commitfest.postgresql.org/).
- [Developer FAQ](https://wiki.postgresql.org/wiki/Developer_FAQ),
  [Submitting a Patch](https://wiki.postgresql.org/wiki/Submitting_a_Patch),
  [Reviewing a Patch](https://wiki.postgresql.org/wiki/Reviewing_a_Patch).

For discussions, search exact symbols, previous names, patch title and symptom.
Use official archive URLs with `site:postgresql.org/message-id`, then open the
thread, not just search snippets. Capture subject, Message-ID/URL, date, version
and relevant replies. Follow commit `Discussion:` links when available. A
CommitFest entry helps locate attachments and review state but does not establish
technical facts. Check the latest relevant version and any prerequisite patches.

Keep a small evidence ledger in the task notes when several claims interact:

| Question | Evidence at revision/date | Finding | Still unknown |
| --- | --- | --- | --- |
| Which path handles the reproducer? | local file/symbol or message URL | observed behavior or qualified inference | untested branch/edge case |

Write human-readable results; do not label every sentence. Explain why a source
supports a claim and what experiment would disprove a hypothesis.
