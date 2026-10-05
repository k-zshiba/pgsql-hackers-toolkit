# Contributor mail preparation

Check the current [submission guide](https://wiki.postgresql.org/wiki/Submitting_a_Patch),
[review guide](https://wiki.postgresql.org/wiki/Reviewing_a_Patch), and the relevant
[pgsql-hackers thread](https://www.postgresql.org/list/pgsql-hackers/).
Use the existing thread's style and substance. An old Wiki example does not
set today's manager, deadline, attachment format or CommitFest procedure.

For replies, preserve Subject/In-Reply-To context in the draft metadata and trim
quotations to the point being answered. Respond below the relevant passage.
Do not turn a small technical reply into a long summary of the entire project.
Email bodies should be readable as plain text; avoid decorative Markdown.

A submission often needs these facts, in natural prose rather than a mandatory
form: what is wrong, what changes, why this approach, how to reproduce/test,
and what still needs discussion. Include base revision and patch version when
they disambiguate the series. Benchmarks need reproducible setup/results, not
unsubstantiated speed claims. WIP means incomplete, not verified readiness.

For a revised series, list changes from the prior version, acknowledge the
specific feedback accurately and retain unresolved points. Never say every
comment was addressed if part remains open. For review mail, focus on defects,
questions and the tested environment; partial reviews can be useful.

Before drafting patch creation commands, inspect existing commits and working
changes. `git format-patch` for a deliberately selected commit range and a
scoped diff for uncommitted work are different operations. Use the branch's
current submission practice, a versioned filename and a separate output
directory. Inspect attachment content and applicability after generating it.
Never run a blanket diff over a tree containing other people's work.

The draft should contain no placeholder evidence presented as fact. Put missing
facts in a note to the user, or explicitly describe the uncertainty in the mail.
Sign with an identity the user supplied; do not invent one.
