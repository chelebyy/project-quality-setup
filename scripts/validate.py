"""Validate this repository's skill packaging using Python's standard library."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "project-quality-setup"


def validate():
    errors = []
    entry = SKILL / "SKILL.md"
    text = entry.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        errors.append("SKILL.md needs YAML frontmatter")
    else:
        metadata = dict(re.findall(r"^(name|description):\s*(.+)$", parts[1], re.M))
        if metadata.get("name") != SKILL.name:
            errors.append("Skill name does not match directory")
        if not metadata.get("description", "").strip():
            errors.append("Missing skill description")
    for required in (ROOT / "LICENSE", ROOT / "README.md", SKILL / "agents" / "openai.yaml"):
        if not required.is_file():
            errors.append(f"Missing {required.relative_to(ROOT)}")
    files = [ROOT / "README.md", *SKILL.rglob("*.md")]
    links = 0
    for path in files:
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\]\(([^\s)]+)\)", content):
            href = match.group(1)
            parsed = urlsplit(href)
            if parsed.scheme or href.startswith("#"):
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f"Broken/escaping link in {path.relative_to(ROOT)}: {href}")
            links += 1
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated skill metadata, packaging and {links} local links.")


if __name__ == "__main__":
    validate()
