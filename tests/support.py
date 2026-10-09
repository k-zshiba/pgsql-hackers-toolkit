"""Small validation helpers; installation/deployment remain APM's responsibility."""

import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "research-postgresql", "design-pg-patch", "implement-pg-patch",
    "test-pg-patch", "review-pg-patch", "prepare-pgsql-hackers-post",
    "revise-pg-patch",
}
CONTRACT = ROOT / ".apm/instructions/postgresql-contributor.instructions.md"
APM_VERSION = "0.33.0"


class UniqueLoader(yaml.SafeLoader):
    """Reject accidentally repeated manifest/frontmatter keys."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_yaml(path):
    return yaml.load(Path(path).read_text(), Loader=UniqueLoader)


def frontmatter(path):
    text = Path(path).read_text()
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    return yaml.load(match[1], Loader=UniqueLoader), match[2]


def markdown_links(text):
    for token in MarkdownIt().parse(text):
        for child in token.children or []:
            if child.type == "link_open":
                yield child.attrGet("href")


def anchors(text):
    found = set()
    counts = {}
    tokens = MarkdownIt().parse(text)
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            heading = tokens[i + 1].content.lower()
            slug = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
            count = counts.get(slug, 0)
            counts[slug] = count + 1
            found.add(slug if count == 0 else f"{slug}-{count}")
    return found


def check_links(paths, boundary):
    """Resolve Markdown links, including deployed references, without network."""
    errors = []
    boundary = Path(boundary).resolve()
    for path in paths:
        for href in markdown_links(path.read_text()):
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
            if not target.is_relative_to(boundary):
                errors.append(f"{path}: link escapes package/project: {href}")
            elif not target.exists():
                errors.append(f"{path}: broken link: {href}")
            elif url.fragment and target.suffix == ".md":
                if unquote(url.fragment) not in anchors(target.read_text()):
                    errors.append(f"{path}: missing anchor: {href}")
    return errors


def copy_source(destination):
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("apm.yml", "apm.lock.yaml", "README.md", "LICENSE", "CHANGELOG.md"):
        shutil.copy2(ROOT / name, destination / name)
    shutil.copytree(ROOT / ".apm", destination / ".apm")
    return destination


class Sandbox:
    """Only child processes use this disposable home; no user config is loaded."""

    def __init__(self, root):
        self.root = Path(root)
        state = self.root / "state"
        state.mkdir()
        (state / "tmp").mkdir()
        git_config = state / "gitconfig"
        git_config.write_text("")
        # Allowlist rather than passing API tokens or user agent configuration.
        self.env = {
            "PATH": str(Path(sys.executable).parent) + os.pathsep + os.defpath,
            "HOME": str(state), "APM_HOME": str(state / ".apm"),
            "TMPDIR": str(state / "tmp"), "LANG": "C.UTF-8",
            "PYTHONUTF8": "1", "NO_COLOR": "1", "GIT_TERMINAL_PROMPT": "0",
            "GIT_CONFIG_GLOBAL": str(git_config), "GIT_CONFIG_NOSYSTEM": "1",
        }
        self.apm = str(Path(sys.executable).with_name("apm"))
        if not Path(self.apm).is_file():
            raise RuntimeError("Run tests with the Python environment containing requirements-dev.txt")

    def run(self, cwd, args, ok=True):
        result = subprocess.run(args, cwd=cwd, env=self.env, text=True,
                                capture_output=True, timeout=60)
        if ok and result.returncode:
            raise AssertionError(f"{args} exited {result.returncode}\n{result.stdout}\n{result.stderr}")
        return result

    def cli(self, cwd, *args, ok=True):
        return self.run(cwd, [self.apm, *args], ok=ok)

    def consumer(self, name, targets, dependency=None):
        path = self.root / name
        path.mkdir()
        self.run(path, ["git", "init", "-q"])
        manifest = {"name": name, "version": "0.0.0", "targets": targets,
                    "dependencies": {"apm": [dependency]} if dependency else {}}
        (path / "apm.yml").write_text(yaml.safe_dump(manifest, sort_keys=False))
        return path


def deployed_snapshot(path):
    files = [path / "apm.lock.yaml", path / "AGENTS.md", path / "CLAUDE.md"]
    for name in (".agents", ".claude", ".codex", ".github"):
        files.extend((path / name).rglob("*"))
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in files if p.is_file()}
