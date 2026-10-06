"""Real APM authoring, packing and consumer tests without global deployment."""

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

import yaml

from support import CONTRACT, ROOT, SKILLS, Sandbox, check_links, copy_source, deployed_snapshot, frontmatter, load_yaml


class APMTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pgsql-toolkit-test-")
        self.addCleanup(self.temp.cleanup)
        self.sandbox = Sandbox(self.temp.name)
        self.source = copy_source(Path(self.temp.name) / "package")

    def assert_deployment(self, consumer, targets):
        roots = []
        if "codex" in targets or "agent-skills" in targets:
            roots.append(consumer / ".agents/skills")
        if "claude" in targets:
            roots.append(consumer / ".claude/skills")
        for root in roots:
            self.assertEqual({p.parent.name for p in root.glob("*/SKILL.md")}, SKILLS)
            self.assertEqual(check_links(root.rglob("*.md"), consumer), [])
            for source in (ROOT / ".apm/skills").glob("*/SKILL.md"):
                dest = root / source.parent.name / "SKILL.md"
                self.assertEqual(frontmatter(source)[0], frontmatter(dest)[0])
                # Apart from APM-managed link relocation, source text must survive.
                from support import markdown_links
                def normalize(text):
                    for href in markdown_links(text):
                        text = text.replace(href, "LINK")
                    return text
                self.assertEqual(normalize(source.read_text()), normalize(dest.read_text()))
                for ref in source.parent.glob("references/*.md"):
                    self.assertEqual(ref.read_bytes(), (dest.parent / "references" / ref.name).read_bytes())
        body = frontmatter(CONTRACT)[1].strip()
        if "codex" in targets:
            text = (consumer / "AGENTS.md").read_text()
            self.assertIn(body, text)
            self.assertEqual(text.count(body), 1)
        if "claude" in targets:
            rule = consumer / ".claude/rules/postgresql-contributor.md"
            self.assertIn(body, rule.read_text())
            if (consumer / "CLAUDE.md").exists():
                self.assertNotIn(body, (consumer / "CLAUDE.md").read_text())
        if "claude" not in targets:
            self.assertFalse((consumer / ".claude").exists())
            self.assertFalse((consumer / "CLAUDE.md").exists())
        if "codex" not in targets:
            self.assertFalse((consumer / "AGENTS.md").exists())
        self.assertFalse((consumer / ".codex/agents").exists())

    def test_manifest_validate_build_frozen_and_pack(self):
        lock = (self.source / "apm.lock.yaml").read_bytes()
        self.sandbox.cli(self.source, "compile", "--validate")
        self.sandbox.cli(self.source, "compile", "--dry-run")
        self.sandbox.cli(self.source, "install", "--frozen")
        self.sandbox.cli(self.source, "compile", "--single-agents")
        self.assert_deployment(self.source, ["codex", "claude"])
        self.sandbox.cli(self.source, "audit", "--ci")
        self.sandbox.cli(self.source, "pack", "--archive", "-o", "dist")
        archive = next((self.source / "dist").glob("*.zip"))
        with zipfile.ZipFile(archive) as packed:
            names = packed.namelist()
            self.assertEqual(sum(name.endswith("SKILL.md") for name in names), 7)
            self.assertTrue(any(name.endswith("instructions/postgresql-contributor.instructions.md") for name in names))
            license_name = next(name for name in names if name.endswith("instructions/LICENSE"))
            self.assertEqual(packed.read(license_name), (ROOT / "LICENSE").read_bytes())
            metadata_name = next(name for name in names if name.endswith("plugin.json"))
            self.assertEqual(json.loads(packed.read(metadata_name))["license"], "PostgreSQL")
            self.assertFalse(any("apm_modules/" in name for name in names))
        # Lock generation alone must reproduce the committed empty closure.
        fresh = Path(self.temp.name) / "lock-only"
        fresh.mkdir()
        shutil.copy2(self.source / "apm.yml", fresh / "apm.yml")
        self.sandbox.cli(fresh, "lock")
        self.assertEqual(lock, (fresh / "apm.lock.yaml").read_bytes())

    def test_local_consumers_and_idempotency(self):
        for targets in (["codex"], ["claude"], ["codex", "claude"], ["agent-skills"]):
            with self.subTest(targets=targets):
                consumer = self.sandbox.consumer("consumer-" + "-".join(targets), targets, "../package")
                self.sandbox.cli(consumer, "install")
                if "codex" in targets:
                    self.sandbox.cli(consumer, "compile", "--single-agents")
                self.assert_deployment(consumer, targets)
                before = deployed_snapshot(consumer)
                self.sandbox.cli(consumer, "install", "--frozen")
                if "codex" in targets:
                    self.sandbox.cli(consumer, "compile", "--single-agents")
                self.assertEqual(before, deployed_snapshot(consumer))
                self.sandbox.cli(consumer, "audit", "--ci")

    def git_fixture(self):
        s = self.sandbox
        s.run(self.source, ["git", "init", "-q"])
        s.run(self.source, ["git", "add", "."])
        s.run(self.source, ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                            "commit", "-qm", "Fixture source"])
        s.run(self.source, ["git", "tag", "v0.1.0"])
        commit = s.run(self.source, ["git", "rev-parse", "HEAD"]).stdout.strip()
        remote = "https://git.example.test/fixture/pgsql-hackers-toolkit.git"
        s.run(self.source, ["git", "config", "--global", f"url.{self.source.as_uri()}.insteadOf", remote])
        s.env["GIT_ALLOW_PROTOCOL"] = "file:https"
        return remote, commit

    def test_git_frozen_replay_drift_and_prune(self):
        remote, commit = self.git_fixture()
        consumer = self.sandbox.consumer("git-consumer", ["codex", "claude"], remote + "#v0.1.0")
        self.sandbox.cli(consumer, "install")
        self.sandbox.cli(consumer, "compile", "--single-agents")
        self.assert_deployment(consumer, ["codex", "claude"])
        lock = load_yaml(consumer / "apm.lock.yaml")
        self.assertEqual(lock["dependencies"][0]["resolved_commit"], commit)
        before = deployed_snapshot(consumer)
        shutil.rmtree(consumer / "apm_modules")  # fixture-owned disposable cache only
        self.sandbox.cli(consumer, "install", "--frozen")
        self.sandbox.cli(consumer, "compile", "--single-agents")
        self.assertEqual(before, deployed_snapshot(consumer))

        manifest_path = consumer / "apm.yml"
        original = manifest_path.read_bytes()
        manifest = load_yaml(manifest_path)
        manifest["dependencies"]["apm"] = [remote + "#v0.2.0"]
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))
        frozen = self.sandbox.cli(consumer, "install", "--frozen", ok=False)
        self.assertNotEqual(frozen.returncode, 0)
        self.assertIn("frozen", (frozen.stdout + frozen.stderr).lower())
        self.assertEqual(before, deployed_snapshot(consumer))
        manifest_path.write_bytes(original)

        deployed = consumer / ".agents/skills/research-postgresql/SKILL.md"
        preserved = deployed.read_bytes()
        deployed.write_bytes(preserved + b"\nManual deployment edit.\n")
        audit = self.sandbox.cli(consumer, "audit", "--ci", ok=False)
        self.assertNotEqual(audit.returncode, 0)
        deployed.write_bytes(preserved)
        self.sandbox.cli(consumer, "audit", "--ci")

        # Prune must remove owned artifacts and preserve unrelated user files.
        sentinel = consumer / ".claude/rules/user.md"
        sentinel.write_text("User-authored rule.\n")
        manifest["dependencies"] = {}
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))
        self.sandbox.cli(consumer, "prune")
        self.assertEqual(sentinel.read_text(), "User-authored rule.\n")
        self.assertFalse((consumer / ".claude/rules/postgresql-contributor.md").exists())
        self.assertEqual(list((consumer / ".agents/skills").glob("*/SKILL.md")), [])
        self.assertEqual(list((consumer / ".claude/skills").glob("*/SKILL.md")), [])
        # Prune leaves compiled roots; recompilation must remove obsolete context.
        body = frontmatter(CONTRACT)[1].strip()
        self.assertIn(body, (consumer / "AGENTS.md").read_text())
        self.sandbox.cli(consumer, "compile", "--single-agents")
        self.assertNotIn(body, (consumer / "AGENTS.md").read_text())

    def test_packed_contents_and_tamper_rejection(self):
        self.sandbox.cli(self.source, "install", "--frozen")
        self.sandbox.cli(self.source, "compile", "--single-agents")
        self.sandbox.cli(self.source, "pack", "-o", "dist")
        bundle = next(p for p in (self.source / "dist").iterdir() if p.is_dir())
        self.assertEqual(check_links(bundle.rglob("*.md"), bundle), [])
        lock = load_yaml(bundle / "apm.lock.yaml")
        for relative, digest in lock["pack"]["bundle_files"].items():
            self.assertEqual(hashlib.sha256((bundle / relative).read_bytes()).hexdigest(), digest)
        self.assertEqual({p.parent.name for p in (bundle / "skills").glob("*/SKILL.md")}, SKILLS)
        for source in (ROOT / ".apm/skills").rglob("*.md"):
            self.assertEqual(source.read_bytes(), (bundle / "skills" / source.relative_to(ROOT / ".apm/skills")).read_bytes())
        self.assertEqual(CONTRACT.read_bytes(),
                         (bundle / "instructions/postgresql-contributor.instructions.md").read_bytes())
        # Full consumer support is tested above through native APM/Git packages.
        # APM 0.33.0 direct bundle install does not relocate cross-Skill links;
        # do not pretend its successful exit code establishes usable deployment.
        tampered = bundle / "skills/research-postgresql/SKILL.md"
        tampered.write_text(tampered.read_text() + "\nAltered after packing.\n")
        fresh = self.sandbox.consumer("tamper-rejection", ["codex"])
        result = self.sandbox.cli(fresh, "install", str(bundle), "--target", "codex", ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((fresh / ".agents/skills").exists())


if __name__ == "__main__":
    unittest.main()
