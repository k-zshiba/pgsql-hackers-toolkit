import importlib.metadata
import re
import subprocess
import unittest

from apm_cli.models.apm_package import APMPackage
from apm_cli.core.errors import UnknownTargetError

from support import APM_VERSION, CONTRACT, ROOT, SKILLS, check_links, frontmatter, load_yaml


class StructureTests(unittest.TestCase):
    def test_required_files_and_current_manifest_loader(self):
        for name in ("apm.yml", "apm.lock.yaml", "README.md", "CONTRIBUTING.md",
                     "LICENSE", ".gitignore", "CHANGELOG.md", "docs/research.md",
                     "docs/architecture.md", "docs/validation.md", "evals/scenarios.json",
                     "evals/README.md", "examples/workflows.md", ".github/workflows/validate.yml"):
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertEqual(importlib.metadata.version("apm-cli"), APM_VERSION)
        package = APMPackage.from_apm_yml(ROOT / "apm.yml", create_config=False)
        self.assertEqual(package.name, "pgsql-hackers-toolkit")
        manifest = load_yaml(ROOT / "apm.yml")
        self.assertRegex(manifest["version"], r"^0\.\d+\.\d+$")
        self.assertEqual(manifest["targets"], ["codex", "claude", "agent-skills"])
        self.assertEqual(manifest["license"], "PostgreSQL")
        self.assertEqual((ROOT / "LICENSE").read_bytes(),
                         (ROOT / ".apm/instructions/LICENSE").read_bytes())
        self.assertEqual(manifest["dependencies"], {})
        self.assertNotIn("devDependencies", manifest)
        self.assertEqual(manifest["includes"], [".apm/instructions/", ".apm/skills/"])
        self.assertEqual(package.get_apm_dependencies(), [])

    def test_lock_closure_and_schema_rejection(self):
        lock = load_yaml(ROOT / "apm.lock.yaml")
        self.assertEqual(lock["dependencies"], [])
        self.assertEqual(lock["deployments"], [])
        self.assertEqual(lock["apm_version"], APM_VERSION)
        manifest = load_yaml(ROOT / "apm.yml")
        for mutation in ({"targets": ["imaginary-agent"]}, {"$schema": "https://invalid.test/schema"}):
            with self.subTest(mutation=mutation), self.assertRaises((ValueError, UnknownTargetError)):
                APMPackage.from_mapping({**manifest, **mutation}, package_path=ROOT, create_config=False)

    def test_skill_metadata_and_progressive_references(self):
        paths = list((ROOT / ".apm/skills").glob("*/SKILL.md"))
        names = []
        linked = set()
        for path in paths:
            metadata, body = frontmatter(path)
            name = metadata["name"]
            names.append(name)
            self.assertEqual(name, path.parent.name)
            self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
            self.assertLessEqual(len(name), 64)
            self.assertIsInstance(metadata["description"], str)
            self.assertTrue(1 <= len(metadata["description"]) <= 1024)
            self.assertEqual(set(metadata), {"name", "description"})
            self.assertLess(len(body.splitlines()), 120)
            self.assertIn("../../instructions/postgresql-contributor.instructions.md", body)
            self.assertNotRegex(body, r"TODO|\[INSERT|!`")
            for ref in path.parent.glob("references/*.md"):
                self.assertIn(f"references/{ref.name}", body)
                linked.add(ref)
        self.assertEqual(set(names), SKILLS)
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(linked, set((ROOT / ".apm/skills").glob("*/references/*.md")))
        metadata, body = frontmatter(CONTRACT)
        self.assertEqual(metadata["applyTo"], "**")
        self.assertLess(len(body.splitlines()), 80)

    def test_links_and_no_provider_source_duplication(self):
        paths = []
        for folder in (".apm", "docs", "examples", "evals"):
            paths.extend((ROOT / folder).rglob("*.md"))
        paths.extend(ROOT.glob("*.md"))
        self.assertEqual(check_links(paths, ROOT), [])
        self.assertEqual({p.name for p in (ROOT / ".apm").iterdir()}, {"skills", "instructions"})
        self.assertEqual(len(list((ROOT / ".apm/instructions").glob("*.instructions.md"))), 1)
        tracked = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                                 capture_output=True, check=True).stdout.decode().split("\0")
        for path in tracked:
            self.assertFalse(re.match(r"^(AGENTS.md|CLAUDE.md|plugin.json|apm_modules/|build/|dist/|\.agents/|\.claude/|\.codex/|\.claude-plugin/|\.codex-plugin/)", path), path)
        for path in (ROOT / ".apm").rglob("*"):
            self.assertFalse(path.is_symlink(), path)

    def test_example_manifests_use_release_and_targets(self):
        for path in (ROOT / "examples").glob("*/apm.yml"):
            manifest = load_yaml(path)
            APMPackage.from_apm_yml(path, create_config=False)
            self.assertEqual(manifest["dependencies"]["apm"],
                             ["k-zshiba/pgsql-hackers-toolkit#v0.1.0"])
            self.assertTrue(set(manifest["targets"]) <= {"codex", "claude", "agent-skills"})


if __name__ == "__main__":
    unittest.main()
