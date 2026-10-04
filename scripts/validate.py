"""Validate this repository's skill packaging using Python's standard library."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    skill_root = root / "skills"
    skills = sorted(path for path in skill_root.iterdir() if path.is_dir()) if skill_root.is_dir() else []
    if not skills:
        errors.append("No skill directories found under skills/")
    for skill in skills:
        entry = skill / "SKILL.md"
        if not entry.is_file():
            errors.append(f"Missing {entry.relative_to(root)}")
            continue
        text = entry.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append(f"{entry.relative_to(root)} needs YAML frontmatter")
        else:
            metadata = dict(re.findall(r"^(name|description):\s*(.+)$", parts[1], re.M))
            if metadata.get("name") != skill.name:
                errors.append(f"Skill name does not match directory: {skill.relative_to(root)}")
            if not metadata.get("description", "").strip():
                errors.append(f"Missing skill description: {skill.relative_to(root)}")
        agent_metadata = skill / "agents" / "openai.yaml"
        if not agent_metadata.is_file():
            errors.append(f"Missing {agent_metadata.relative_to(root)}")
    for required in (root / "LICENSE", root / "README.md"):
        if not required.is_file():
            errors.append(f"Missing {required.relative_to(root)}")
    files = [root / "README.md", *(path for skill in skills for path in skill.rglob("*.md"))]
    links = 0
    for path in files:
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\]\(([^\s)]+)\)", content):
            href = match.group(1)
            parsed = urlsplit(href)
            if parsed.scheme or href.startswith("#"):
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root) or not target.exists():
                errors.append(f"Broken/escaping link in {path.relative_to(root)}: {href}")
            links += 1
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(skills)} skill(s), packaging and {links} local links.")


if __name__ == "__main__":
    validate()
