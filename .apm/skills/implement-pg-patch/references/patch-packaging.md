# Package a PostgreSQL patch

When asked to produce a patch attachment, use `git format-patch` from real,
deliberately selected commits. A scoped `git diff` is useful during development,
but do not deliver it with a hand-written mail header as the submission patch.
An explicit user request for another format takes precedence.

Follow Peter Eisentraut's
[How to submit a patch by email, 2023 edition](https://peter.eisentraut.org/blog/2023/05/09/how-to-submit-a-patch-by-email-2023-edition)
for patch generation: commit the intended changes, then use `git format-patch`
with the base branch and `-vN` for versioned submissions.

## Select the changes and metadata

Inspect the base revision, working tree, index and intended commit range. Include
only the reviewed implementation, tests and documentation. Exclude unrelated user
work, generated agent files, build output and private logs. Existing commits must
actually contain the final tested changes; `format-patch` omits uncommitted edits.

Use the real author's identity from the user's instructions, existing commits or
explicit Git author configuration. Preserve authorship when revising another
contributor's work. Do not invent an author name, email, commit ID or date. If the
identity is missing, prepare the diff and message first, then ask for that identity
before generating the final attachment.

For uncommitted changes, or a revision that would require changing the user's
history, transfer only the reviewed diff into an isolated temporary repository
at the verified base. Create local packaging commits there with the established
author identity and the final commit message. A request for a patch file permits
this local packaging step; it does not authorize committing, amending, rebasing
or changing the index in the user's checkout. Report where the packaging commits
were created. Do not change the user's Git configuration.

## Generate and inspect the attachment

Write a concise commit title and a body explaining the concrete problem, resulting
behavior and rationale. Include material limitations. Keep mail greetings, revision
changelogs and conversation-specific notes in the submission email or cover letter.

Inspect the commits selected by the base branch before generating attachments.
When `master` is the verified base branch and all selected commits belong to the
submission, use the article's commands:

```sh
git format-patch master
git format-patch -v1 master
git format-patch -v2 master
```

These are alternatives: use `-v1` for an initial versioned submission and `-v2`,
`-v3`, etc. for revisions. Keep Git's generated `vN-0001-Subject.patch` filenames
and default diffstats. Use the verified target branch or base revision instead
of `master` when appropriate. Add `-o` to write into a separate output directory;
`--base` is optional metadata, as described in the article.

When the intended series needs an explicit range, use the verified base and tip.
For example, with those shell variables resolved:

```sh
git format-patch -v1 --base="$patch_base" -o "$patch_output" "${patch_base}..${patch_tip}"
```

Do not assume that `HEAD` or every commit since an upstream branch belongs in the
patch. Preserve earlier versions in a separate output directory.

Let Git generate the `From <commit-id> Mon Sep 17 00:00:00 2001` separator,
`From:`, `Date:` and `Subject:` headers, commit-message body, `---`, diffstat,
file modes and diff. The separator's date is a format marker, not the author date.
Check the version and, for a series, sequence numbers such as `[PATCH v2 4/7]`.
Do not fabricate metadata or manually force series numbering on a single patch.

Inspect every attachment against the reviewed diff and commit message. Verify
application to the recorded base with `git am` in an isolated repository;
for a series, apply patches in order. Check whitespace and that the generated
diffstat and new-file entries agree with the contents. Return the exact attachment
paths, base, version, validation evidence and unresolved limitations. Packaging
does not imply that tests were rerun or that posting is authorized.
