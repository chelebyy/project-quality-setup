"""Validate collection metadata, local Markdown links and catalog completeness."""
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import yaml

ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = re.compile(r"\A---[ \t]*\n(.*?)^---[ \t]*(?:\n|\Z)", re.M | re.S)
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML construction that refuses ambiguous, duplicate mapping keys."""

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, yaml.MappingNode):
            return super().construct_mapping(node, deep=deep)
        self.flatten_mapping(node)
        seen = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in seen
                seen.add(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    None, None, "unhashable mapping key", key_node.start_mark
                ) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    None, None, "duplicate mapping key", key_node.start_mark
                )
        return super().construct_mapping(node, deep=deep)


def yaml_mapping(text, label, errors):
    try:
        value = yaml.load(text, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        errors.append(f"Invalid YAML in {label}: {getattr(exc, 'problem', None) or type(exc).__name__}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"Expected YAML mapping in {label}")
        return {}
    return value


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def validate_frontmatter(text, skill, root, errors):
    label = (skill / "SKILL.md").relative_to(root)
    match = FRONTMATTER.match(text)
    if not match:
        errors.append(f"{label} needs delimited YAML frontmatter")
        return
    metadata = yaml_mapping(match[1], label, errors)
    name = metadata.get("name")
    if not isinstance(name, str) or not NAME.fullmatch(name) or len(name) > 64:
        errors.append(f"Invalid skill name in {label}")
    if name != skill.name:
        errors.append(f"Skill name does not match directory: {skill.relative_to(root)}")
    description = metadata.get("description")
    if not nonempty_string(description):
        errors.append(f"Missing/non-string skill description in {label}")
    elif len(description.strip()) > 1024:
        errors.append(f"Skill description exceeds 1024 characters in {label}")


def validate_agent(text, skill, root, errors):
    label = (skill / "agents" / "openai.yaml").relative_to(root)
    metadata = yaml_mapping(text, label, errors)
    interface = metadata.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"Expected interface mapping in {label}")
        return
    # This collection requires these UI fields; this is not the entire host schema.
    for field in ("display_name", "short_description", "default_prompt"):
        if not nonempty_string(interface.get(field)):
            errors.append(f"Missing/non-string interface.{field} in {label}")
    short = interface.get("short_description")
    if isinstance(short, str) and not 25 <= len(short) <= 64:
        errors.append(f"interface.short_description must be 25-64 characters in {label}")
    prompt = interface.get("default_prompt")
    if isinstance(prompt, str) and not re.search(
        rf"\${re.escape(skill.name)}(?![\w-])", prompt
    ):
        errors.append(f"interface.default_prompt must mention ${skill.name} in {label}")
    if "policy" in metadata:
        policy = metadata["policy"]
        if not isinstance(policy, dict):
            errors.append(f"Expected policy mapping in {label}")
        elif "allow_implicit_invocation" in policy and not isinstance(
            policy["allow_implicit_invocation"], bool
        ):
            errors.append(f"policy.allow_implicit_invocation must be boolean in {label}")


class ExplicitAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and (name == "id" or (tag == "a" and name == "name")):
                self.anchors.add(value)


def inline_text(tokens):
    return "".join(
        inline_text(token.children) if token.children else
        token.content if token.type in {"text", "code_inline"} else
        " " if token.type in {"softbreak", "hardbreak"} else ""
        for token in tokens
    )


def heading_slug(text):
    # GitHub-style heading IDs for this collection's CommonMark headings.
    return "".join(
        char for char in text.lower()
        if char in " _-" or unicodedata.category(char)[0] in "LNM"
    ).replace(" ", "-")


@dataclass
class MarkdownDocument:
    links: list[tuple[str, str]]
    anchors: set[str]


def parse_markdown(text):
    match = FRONTMATTER.match(text)
    tokens = MarkdownIt("commonmark").enable("table").parse(text[match.end():] if match else text)
    links = []
    headings = set()
    html = ExplicitAnchors()
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            slug = base = heading_slug(inline_text(tokens[index + 1].children or []))
            suffix = 0
            while slug in headings:
                suffix += 1
                slug = f"{base}-{suffix}"
            headings.add(slug)
        if token.type == "html_block":
            html.feed(token.content)
        for child in token.children or []:
            if child.type == "link_open":
                links.append((child.attrGet("href") or "", "link"))
            elif child.type == "image":
                links.append((child.attrGet("src") or "", "image"))
            elif child.type == "html_inline":
                html.feed(child.content)
    return MarkdownDocument(links, headings | html.anchors)


def local_target(source, href):
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None
    path = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source.resolve()
    return path, unquote(parsed.fragment)


def validate(root=ROOT):
    root = Path(root).resolve()
    errors = []
    contents = {}
    documents = {}

    def read(path):
        if path in contents:
            return contents[path]
        if not path.resolve().is_relative_to(root):
            errors.append(f"Path escapes repository: {path.relative_to(root)}")
            contents[path] = ""
            return ""
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            errors.append(f"Missing/unreadable UTF-8 file: {path.relative_to(root)}")
            text = ""
        contents[path] = text
        return text

    def document(path):
        if path not in documents:
            documents[path] = parse_markdown(read(path))
        return documents[path]

    skill_root = root / "skills"
    skills = sorted(path for path in skill_root.iterdir() if path.is_dir()) if skill_root.is_dir() else []
    if not skills:
        errors.append("No skill directories found under skills/")
    for skill in skills:
        validate_frontmatter(read(skill / "SKILL.md"), skill, root, errors)
        validate_agent(read(skill / "agents" / "openai.yaml"), skill, root, errors)
    for required in (root / "LICENSE", root / "README.md"):
        read(required)

    files = [root / "README.md", *(path for skill in skills for path in skill.rglob("*.md"))]
    if (root / "evals" / "README.md").is_file():
        files.append(root / "evals" / "README.md")
    links = 0
    catalog = set()
    for path in files:
        for href, kind in document(path).links:
            try:
                target = local_target(path, href)
            except ValueError:
                errors.append(f"Invalid link in {path.relative_to(root)}: {href}")
                continue
            if target is None:
                continue
            destination, anchor = target
            links += 1
            if not destination.is_relative_to(root) or not destination.exists():
                errors.append(f"Broken/escaping link in {path.relative_to(root)}: {href}")
                continue
            if anchor and destination.suffix.lower() == ".md" and destination.is_file():
                if anchor not in document(destination).anchors:
                    errors.append(f"Missing Markdown anchor in {path.relative_to(root)}: {href}")
            if path == root / "README.md" and kind == "link":
                catalog.add(destination)
    for skill in skills:
        if (skill / "SKILL.md").resolve() not in catalog:
            errors.append(f"README catalog missing skill: {skill.name}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(skills)} skill(s), metadata, catalog and {links} local links.")


if __name__ == "__main__":
    validate()
