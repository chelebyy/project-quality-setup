"""Preparation safety and corpus integrity, not model behavior evaluations."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts.eval_cases import ROOT, SUITE, hashes, load_suite, prepare


class EvaluationInputsTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def test_every_case_can_be_prepared_without_rubric_or_behavior_claim(self):
        suite = load_suite()
        for case in suite["cases"]:
            with self.subTest(case=case["id"]):
                output = self.root / case["id"]
                record = prepare(case["id"], output)
                self.assertEqual(record["status"], "not_run")
                self.assertEqual(record["project_sha256"], hashes(output / "project"))
                self.assertEqual(record["skill_sha256"], hashes(output / "skill"))
                task = (output / "TASK.md").read_text(encoding="utf-8")
                self.assertIn(case["prompt"], task)
                for rubric_line in case["checks"] + case["forbidden"]:
                    self.assertNotIn(rubric_line, task)
                self.assertFalse((output / "cases.json").exists())
                self.assertFalse((output / "result.json").exists())

    def test_existing_output_is_never_overwritten(self):
        output = self.root / "existing"
        output.mkdir()
        marker = output / "keep.txt"
        marker.write_text("preserve", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            prepare("audit-only", output)
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")
        self.assertEqual(list(output.iterdir()), [marker])

    def test_unknown_case_does_not_create_output(self):
        output = self.root / "unknown"
        with self.assertRaisesRegex(ValueError, "Unknown evaluation case"):
            prepare("no-such-case", output)
        self.assertFalse(output.exists())

    def test_preparation_does_not_modify_original_skill_or_fixture(self):
        fixture = SUITE.parent / "fixtures" / "backend"
        skill = ROOT / "skills" / "project-quality-setup"
        before = (hashes(fixture), hashes(skill))
        prepare("audit-only", self.root / "copy")
        self.assertEqual((hashes(fixture), hashes(skill)), before)

    def test_protected_output_locations_are_rejected(self):
        for folder in ("skills", "evals", ".git"):
            with self.subTest(folder=folder):
                with self.assertRaisesRegex(ValueError, "must not modify"):
                    prepare("audit-only", ROOT / folder / "do-not-create-eval")

    def test_duplicate_ids_and_traversal_fixtures_are_rejected(self):
        suite = json.loads(SUITE.read_text(encoding="utf-8"))
        original = suite["cases"][0]
        (self.root / "fixtures" / "backend").mkdir(parents=True)
        (self.root / "fixtures" / "backend" / "file.txt").write_text("example", encoding="utf-8")
        suite_path = self.root / "cases.json"
        invalid_cases = (
            [original, original],
            [{**original, "fixture": "../outside"}],
            [{**original, "checks": []}],
            [{**original, "forbidden": [False]}],
            [{**original, "prompt": ""}],
        )
        for cases in invalid_cases:
            with self.subTest(cases=cases):
                suite_path.write_text(json.dumps({**suite, "cases": cases}), encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_suite(suite_path)


if __name__ == "__main__":
    unittest.main()
