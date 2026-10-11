"""Exercise release notes with real Git history and publishing without network writes."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from support import ROOT, Sandbox, load_yaml


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pgsql-toolkit-release-")
        self.addCleanup(self.temp.cleanup)
        self.sandbox = Sandbox(self.temp.name)
        self.repo = Path(self.temp.name) / "repository"
        self.repo.mkdir()
        self.sandbox.run(self.repo, ["git", "init", "-q", "-b", "main"])

    def git(self, *args):
        return self.sandbox.run(self.repo, ["git", *args]).stdout.strip()

    def commit(self, subject):
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "--allow-empty", "-qm", subject)
        return self.git("rev-parse", "HEAD")

    def notes(self, tag, ok=True):
        return self.sandbox.run(self.repo, [
            sys.executable, str(ROOT / ".github/scripts/release_notes.py"),
            tag, "https://github.com/example/toolkit",
        ], ok=ok)

    def test_initial_release_and_invalid_tags(self):
        sha = self.commit("Initial source")
        self.git("tag", "v0.1.0")
        notes = self.notes("v0.1.0").stdout
        self.assertIn("Changes in v0.1.0.", notes)
        self.assertIn(f"/commit/{sha}", notes)
        self.assertIn("Initial source", notes)
        self.assertNotIn("/compare/", notes)
        for tag in ("v01.1.0", "v0.1.0-rc1", "0.1.0", "v0.1.0;echo bad"):
            with self.subTest(tag=tag):
                result = self.notes(tag, ok=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
        self.assertNotEqual(self.notes("v0.1.1", ok=False).returncode, 0)

    def test_numeric_previous_version_and_reachable_history(self):
        self.commit("Old release")
        self.git("tag", "v0.1.9")
        self.commit("Previous release")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "tag", "-a", "v0.1.10", "-m", "Annotated version tag")
        self.git("tag", "v9.0.0")
        self.git("tag", "v0.1.99-rc1")
        self.git("switch", "--orphan", "unrelated")
        self.commit("Unrelated branch")
        self.git("tag", "v0.1.99")
        self.git("switch", "main")
        sha = self.commit("Keep *literal* <script> $(touch nope)")
        self.git("tag", "v0.2.0")
        notes = self.notes("v0.2.0").stdout
        self.assertIn("/compare/v0.1.10...v0.2.0", notes)
        self.assertIn(f"/commit/{sha}", notes)
        self.assertIn(r"Keep \*literal\* \<script\> $\(touch nope\)", notes)
        for excluded in ("Old release", "Previous release", "Unrelated branch"):
            self.assertNotIn(excluded, notes)
        self.assertFalse((self.repo / "nope").exists())
        self.git("tag", "v0.2.1")
        self.assertIn("No new commits", self.notes("v0.2.1").stdout)

    def test_publish_creates_once_preserves_existing_and_reports_failure(self):
        workflow = load_yaml(ROOT / ".github/workflows/validate.yml")
        publish = workflow["jobs"]["release"]["steps"][-1]["run"]
        binary_dir = Path(self.temp.name) / "bin"
        binary_dir.mkdir()
        fake_gh = binary_dir / "gh"
        fake_gh.write_text(
            f"#!{sys.executable}\n"
            "import json, os, sys\n"
            "with open(os.environ['GH_LOG'], 'a') as log:\n"
            "    log.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            "sys.exit(int(os.environ['VIEW_EXIT' if sys.argv[2] == 'view' else 'CREATE_EXIT']))\n"
        )
        fake_gh.chmod(0o755)
        log = Path(self.temp.name) / "gh-log"
        env = dict(self.sandbox.env, PATH=str(binary_dir) + os.pathsep + os.defpath,
                   GH_LOG=str(log), RELEASE_TAG="v0.2.0", RUNNER_TEMP=self.temp.name,
                   CREATE_EXIT="0")
        for view_exit, create_exit, expected_calls, expected_exit in (
            ("1", "0", 2, 0), ("0", "0", 1, 0), ("1", "1", 2, 1),
        ):
            with self.subTest(view_exit=view_exit, create_exit=create_exit):
                log.write_text("")
                result = subprocess.run(["bash", "-e", "-c", publish], cwd=self.repo,
                                        env=dict(env, VIEW_EXIT=view_exit, CREATE_EXIT=create_exit),
                                        text=True, capture_output=True, timeout=10)
                self.assertEqual(result.returncode, expected_exit, result.stderr)
                calls = [json.loads(line) for line in log.read_text().splitlines()]
                self.assertEqual(len(calls), expected_calls)
                if expected_calls == 2:
                    self.assertEqual(calls[1], ["release", "create", "v0.2.0", "--verify-tag",
                                               "--title", "v0.2.0", "--notes-file",
                                               str(Path(self.temp.name) / "release-notes.md")])


if __name__ == "__main__":
    unittest.main()
