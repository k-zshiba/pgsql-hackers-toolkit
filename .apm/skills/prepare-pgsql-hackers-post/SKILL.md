---
name: prepare-pgsql-hackers-post
description: Draft a pgsql-hackers initial core proposal, patch submission, revised patch description, review email or reviewer response grounded in current source and discussion. Use to prepare contributor communication, not to send it. Do not use for PostgreSQL marketing, application support or database administration mail.
---

# Prepare a pgsql-hackers post

Read the [common contributor contract](../../instructions/postgresql-contributor.instructions.md).
Load [mail preparation](references/mail-preparation.md) for the chosen message
type. Establish audience, existing thread/Message-ID, patch version/base,
verified behavior, validation evidence and unresolved questions.

Read recent relevant pgsql-hackers messages and the current submission/review
guidance. Preserve the thread and reply context when responding. Use plain,
concise technical prose and trimmed inline quotations; avoid marketing claims,
invented acknowledgments, fake sign-offs and statements of unperformed testing.

Select what the recipient needs:

- Initial proposal: observed problem, current/desired semantics, alternatives and
  questions seeking design feedback, before a large nontrivial implementation.
- Submission: problem, behavior change, rationale, version/base, patch series,
  docs/tests, actual validation and remaining limitations.
- Revision: material changes since the prior version, responses linked to
  feedback, exact attachments and still-open issues.
- Review/response: concrete findings or point-by-point technical replies with
  reproducer/evidence; distinguish questions, addressed feedback and disagreement.

Verify local attachments match the described version and intended diff. Do not
guess filenames, generate a patch containing unrelated work, or include private
logs/credentials. If no tested patch is available, clearly frame the message as
an early proposal/WIP and explain what evidence is missing.

Return the draft subject/body and attachment list, with any factual gaps outside
the draft. Do not send email, post to the list, register/update CommitFest or
publish attachments merely because a draft was requested. If explicitly asked
to send, verify the concrete recipients, body and attachments and execute only
the authorized action under the available tool's authorization policy.
