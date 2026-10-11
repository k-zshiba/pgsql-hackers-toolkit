"""Generate GitHub Release notes from the previous reachable version tag."""

import argparse
import re
import subprocess


VERSION_TAG = re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def version(tag):
    match = VERSION_TAG.fullmatch(tag)
    return tuple(map(int, match.groups())) if match else None


def git(*args):
    return subprocess.run(["git", *args], check=True, text=True,
                          capture_output=True).stdout.strip()


def release_notes(tag, repository_url):
    current_version = version(tag)
    if current_version is None:
        raise ValueError("Release tag must be vMAJOR.MINOR.PATCH without leading zeros")
    current_ref = f"refs/tags/{tag}"
    git("rev-parse", "--verify", f"{current_ref}^{{commit}}")
    candidates = [candidate for candidate in git("tag", "--merged", current_ref).splitlines()
                  if version(candidate) is not None and version(candidate) < current_version]
    previous = max(candidates, key=version) if candidates else None
    revision = f"refs/tags/{previous}..{current_ref}" if previous else current_ref
    commits = git("log", "--reverse", "--format=%H%x00%s", revision)
    repository_url = repository_url.rstrip("/")
    lines = [f"Changes in {tag}.", "", "## Commits", ""]
    if commits:
        for commit in commits.split("\n"):
            sha, subject = commit.split("\0", 1)
            subject = re.sub(r"([\\`*_{}\[\]()<>#!|])", r"\\\1", subject)
            lines.append(f"- {subject} ([{sha[:7]}]({repository_url}/commit/{sha}))")
    else:
        lines.append("No new commits since the previous version tag.")
    if previous:
        lines.extend(["", f"[Full changelog]({repository_url}/compare/{previous}...{tag})"])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag")
    parser.add_argument("repository_url")
    args = parser.parse_args()
    try:
        print(release_notes(args.tag, args.repository_url), end="")
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Cannot generate release notes: {error}\n")


if __name__ == "__main__":
    main()
