"""Regression checks for collection packaging and real rejected/accepted inputs."""
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
        (skill / "agents" / "openai.yaml").write_text(
            'interface:\n  display_name: "Example"\n'
            '  short_description: "Example skill for validation tests"\n'
            f'  default_prompt: "Use ${name} to assess this project."\n',
            encoding="utf-8",
        )
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Example skill\n---\n# Example\n",
            encoding="utf-8",
        )
        with (self.root / "README.md").open("a", encoding="utf-8") as catalog:
            catalog.write(f"\n[{name}](skills/{name}/SKILL.md)\n")
        return skill

    def assert_valid(self):
        with redirect_stdout(StringIO()):
            validate(self.root)

    def set_entry(self, metadata, body="# Example\n"):
        (self.root / "skills" / "example" / "SKILL.md").write_text(
            f"---\n{metadata}\n---\n{body}", encoding="utf-8"
        )

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

    def test_empty_or_non_string_descriptions_are_rejected(self):
        self.add_skill("example")
        for value in ('""', '"   "', "|", ">", "null", "false", "123", "[]", "{}"):
            with self.subTest(value=value):
                self.set_entry(f"name: example\ndescription: {value}")
                with self.assertRaisesRegex(SystemExit, "skill description"):
                    validate(self.root)

    def test_quoted_names_and_multiline_descriptions_are_supported(self):
        self.add_skill("example")
        for description in ('"Contains --- within a scalar"', "|\n  First line.\n  Second line.", ">\n  Folded\n  description."):
            with self.subTest(description=description):
                self.set_entry(f'name: "example"\ndescription: {description}\nmetadata:\n  category: quality')
                self.assert_valid()

    def test_malformed_or_unsafe_yaml_is_rejected(self):
        self.add_skill("example")
        for metadata in (
            "name: example\ndescription: [unterminated",
            "name: example\nname: example\ndescription: Valid",
            "name: example\ndescription: Valid\nmetadata:\n  key: 1\n  key: 2",
            "name: example\ndescription: !!python/object:builtins.str {}",
            "name: example\ndescription: invalid\x00character",
        ):
            with self.subTest(metadata=metadata):
                self.set_entry(metadata)
                with self.assertRaisesRegex(SystemExit, "Invalid YAML"):
                    validate(self.root)

    def test_non_mapping_frontmatter_and_missing_delimiter_are_rejected(self):
        skill = self.add_skill("example")
        for text in ("---\n- name\n---\n", "---\nname: example\ndescription: Text\n", "name: example\n"):
            with self.subTest(text=text):
                (skill / "SKILL.md").write_text(text, encoding="utf-8")
                with self.assertRaises(SystemExit):
                    validate(self.root)

    def test_missing_entry_agent_and_license_are_reported(self):
        skill = self.add_skill("example")
        (skill / "SKILL.md").unlink()
        (skill / "agents" / "openai.yaml").unlink()
        (self.root / "LICENSE").unlink()
        with self.assertRaises(SystemExit) as result:
            validate(self.root)
        for filename in ("SKILL.md", "openai.yaml", "LICENSE"):
            self.assertIn(filename, str(result.exception))

    def test_empty_or_wrong_agent_metadata_is_rejected(self):
        skill = self.add_skill("example")
        agent = skill / "agents" / "openai.yaml"
        original = agent.read_text(encoding="utf-8")
        for text in (
            "", "[]", "interface: {}", "interface: false", "interface: [",
            original.replace('display_name: "Example"', "display_name: 42"),
            original.replace("Example skill for validation tests", "Too short"),
            original.replace("$example", "$example-other"),
            original.replace("$example", "$example_other"),
            original.replace("$example", "$exampleOther"),
            original + 'policy:\n  allow_implicit_invocation: "false"\n',
            original + 'policy: []\n',
            original + 'interface: {}\n',
        ):
            with self.subTest(text=text):
                agent.write_text(text, encoding="utf-8")
                with self.assertRaises(SystemExit):
                    validate(self.root)

    def test_optional_agent_fields_are_preserved_and_valid(self):
        skill = self.add_skill("example")
        agent = skill / "agents" / "openai.yaml"
        with agent.open("a", encoding="utf-8") as output:
            output.write('policy:\n  allow_implicit_invocation: false\ndependencies:\n  tools: []\n')
        original = agent.read_bytes()
        self.assert_valid()
        self.assertEqual(agent.read_bytes(), original)

    def test_catalog_must_link_every_skill_outside_code_examples(self):
        self.add_skill("example")
        for text in (
            "# Skills\n",
            "# Skills\n```md\n[Example](skills/example/SKILL.md)\n```\n",
            "# Skills\n![Example](skills/example/SKILL.md)\n",
        ):
            with self.subTest(text=text):
                (self.root / "README.md").write_text(text, encoding="utf-8")
                with self.assertRaisesRegex(SystemExit, "README catalog missing skill: example"):
                    validate(self.root)

    def test_reference_catalog_links_are_supported(self):
        self.add_skill("example")
        (self.root / "README.md").write_text(
            '# Skills\n[Example][skill]\n\n[skill]: skills/example/SKILL.md "Example skill"\n',
            encoding="utf-8",
        )
        self.assert_valid()

    def test_missing_same_file_and_cross_file_anchors_are_rejected(self):
        skill = self.add_skill("example")
        (skill / "guide.md").write_text("# Existing\n", encoding="utf-8")
        for target in ("#missing", "guide.md#missing"):
            with self.subTest(target=target):
                self.set_entry("name: example\ndescription: Valid", f"# Example\n[Missing]({target})\n")
                with self.assertRaisesRegex(SystemExit, "Missing Markdown anchor"):
                    validate(self.root)

    def test_headings_duplicates_unicode_and_explicit_anchors(self):
        self.add_skill("example")
        self.set_entry("name: example\ndescription: Valid", """# Hello *world* `code`!
## Hello world code!
## Türkçe bölüm
Setext heading
--------------
<a id="custom-anchor"></a>

[First](#hello-world-code)
[Duplicate](#hello-world-code-1)
[Unicode](#t%C3%BCrk%C3%A7e-b%C3%B6l%C3%BCm)
[Setext](#setext-heading)
[Explicit](#custom-anchor)
""")
        self.assert_valid()

    def test_encoded_paths_and_reference_links_are_checked(self):
        skill = self.add_skill("example")
        guide = skill / "guide (draft).md"
        guide.write_text("# Target\n", encoding="utf-8")
        self.set_entry("name: example\ndescription: Valid", """# Example
[Guide](<guide (draft).md#target>)
[Encoded](guide%20%28draft%29.md#target)
[Reference][guide]

[guide]: <guide (draft).md#target>
""")
        self.assert_valid()
        guide.unlink()
        with self.assertRaisesRegex(SystemExit, "Broken/escaping link"):
            validate(self.root)

    def test_escape_and_missing_image_are_rejected(self):
        self.add_skill("example")
        for link in ("[Escape](../../../outside.md)", "![Image](missing.png)"):
            with self.subTest(link=link):
                self.set_entry("name: example\ndescription: Valid", "# Example\n" + link)
                with self.assertRaisesRegex(SystemExit, "Broken/escaping link"):
                    validate(self.root)

    def test_code_examples_and_remote_links_do_not_require_local_files(self):
        self.add_skill("example")
        self.set_entry("name: example\ndescription: Valid", """# Example
`[Example](not-a-file.md)`

```md
[Example](not-a-file.md)
```

[Remote](https://example.invalid/docs#external)
[Network](//example.invalid/docs)
[Mail](mailto:example@example.invalid)
""")
        self.assert_valid()

    def test_relative_root_argument_is_supported(self):
        # Path normalization must happen before is_relative_to boundary checks.
        self.add_skill("example")
        with redirect_stdout(StringIO()):
            validate(self.root / "skills" / "..")


if __name__ == "__main__":
    unittest.main()
