"""Regression checks for validating all skills in a collection."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import tempfile
import unittest

from scripts.validate import validate


class CollectionValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        (self.root / "LICENSE").write_text("MIT", encoding="utf-8")
        (self.root / "README.md").write_text("# Skills", encoding="utf-8")

    def add_skill(self, name):
        skill = self.root / "skills" / name
        (skill / "agents").mkdir(parents=True)
        (skill / "agents" / "openai.yaml").write_text("interface: {}", encoding="utf-8")
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Example skill\n---\n# Example\n",
            encoding="utf-8",
        )
        return skill

    def test_valid_collection_includes_second_skill(self):
        self.add_skill("first")
        self.add_skill("second")
        output = StringIO()
        with redirect_stdout(output):
            validate(self.root)
        self.assertIn("Validated 2 skill(s)", output.getvalue())

    def test_invalid_second_skill_is_rejected(self):
        self.add_skill("first")
        second = self.add_skill("second")
        (second / "SKILL.md").write_text(
            "---\nname: wrong-name\ndescription: Example\n---\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(SystemExit, "name does not match directory: skills[/\\\\]second"):
            validate(self.root)

    def test_broken_link_in_second_skill_reference_is_rejected(self):
        self.add_skill("first")
        second = self.add_skill("second")
        (second / "references").mkdir()
        (second / "references" / "guide.md").write_text("[Missing](missing.md)", encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "Broken/escaping link.*guide.md"):
            validate(self.root)

    def test_empty_collection_is_rejected(self):
        with self.assertRaisesRegex(SystemExit, "No skill directories"):
            validate(self.root)


if __name__ == "__main__":
    unittest.main()
