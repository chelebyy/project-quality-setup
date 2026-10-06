"""Validate or prepare isolated evaluation inputs; never run or grade an agent."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "evals" / "project-quality-setup" / "cases.json"
IDENTIFIER = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def safe_files(directory, boundary=None):
    if boundary is not None and not directory.resolve().is_relative_to(boundary.resolve()):
        raise ValueError(f"Evaluation inputs escape their source tree: {directory}")
    if not directory.is_dir() or directory.is_symlink() or directory.is_junction():
        raise ValueError(f"Expected an ordinary fixture/skill directory: {directory}")
    root = directory.resolve()
    files = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink() or path.is_junction() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Links are not allowed in evaluation inputs: {path}")
        if ".git" in path.relative_to(directory).parts:
            raise ValueError("Evaluation inputs must not include Git metadata")
        if path.is_file():
            files.append(path)
    if not files:
        raise ValueError(f"Empty evaluation input directory: {directory}")
    return files


def load_suite(path=SUITE):
    path = Path(path).resolve()
    suite = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(suite, dict) or suite.get("version") != 1:
        raise ValueError("Evaluation suite must be a version 1 object")
    if not isinstance(suite.get("skill"), str) or not IDENTIFIER.fullmatch(suite["skill"]):
        raise ValueError("Invalid evaluation skill name")
    cases = suite.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Evaluation suite needs a nonempty cases list")
    seen = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Each evaluation case must be an object")
        for field in ("id", "fixture"):
            if not isinstance(case.get(field), str) or not IDENTIFIER.fullmatch(case[field]):
                raise ValueError(f"Invalid case {field}")
        if case["id"] in seen:
            raise ValueError(f"Duplicate evaluation case: {case['id']}")
        seen.add(case["id"])
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError(f"Missing prompt: {case['id']}")
        for field in ("checks", "forbidden"):
            values = case.get(field)
            if not isinstance(values, list) or not values or any(
                not isinstance(value, str) or not value.strip() for value in values
            ):
                raise ValueError(f"Missing/non-string {field}: {case['id']}")
        safe_files(path.parent / "fixtures" / case["fixture"], path.parent)
    return suite


def hashes(directory):
    return {
        path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in safe_files(directory)
    }


def copy_inputs(source, destination):
    files = safe_files(source)
    destination.mkdir()
    for path in files:
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)


def prepare(case_id, output, suite_path=SUITE):
    suite_path = Path(suite_path).resolve()
    suite = load_suite(suite_path)
    case = next((item for item in suite["cases"] if item["id"] == case_id), None)
    if case is None:
        raise ValueError(f"Unknown evaluation case: {case_id}")
    repo = suite_path.parents[2]
    skill = repo / "skills" / suite["skill"]
    if not (skill / "SKILL.md").is_file():
        raise ValueError("Evaluation skill entrypoint is missing")
    safe_files(skill, repo)
    output = Path(output).resolve()
    if any(output.is_relative_to(repo / name) for name in ("skills", "evals", ".git")):
        raise ValueError("Evaluation output must not modify skill, suite or Git metadata directories")
    # Never overwrite or clean up an existing evaluation, even an empty directory.
    output.mkdir(parents=True, exist_ok=False)
    copy_inputs(suite_path.parent / "fixtures" / case["fixture"], output / "project")
    copy_inputs(skill, output / "skill")
    task = (
        f"Use ${suite['skill']} at {(output / 'skill' / 'SKILL.md').as_posix()}.\n\n"
        "Work only in the project/ directory; treat the skill snapshot as read-only. "
        "The supplied repository/run data are synthetic offline snapshots, not live evidence. "
        "Do not access external services, network, credentials, production or other repositories; "
        "do not install dependencies. Follow the user's mutation limits below. "
        "Use only the prepared inputs, not the evaluation suite or grader rubric. "
        "Respond in the language of the user request below.\n\n"
        "User request:\n" + case["prompt"] + "\n"
    )
    (output / "TASK.md").write_text(task, encoding="utf-8")
    record = {
        "case": case_id,
        "status": "not_run",
        "suite_sha256": hashlib.sha256(suite_path.read_bytes()).hexdigest(),
        "project_sha256": hashes(output / "project"),
        "skill_sha256": hashes(output / "skill"),
        "note": "Prepared inputs only; no agent execution or behavioral success is implied.",
    }
    (output / "run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=SUITE)
    parser.add_argument("--prepare", metavar="CASE")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if bool(args.prepare) != bool(args.output):
        parser.error("--prepare and --output must be supplied together")
    try:
        if args.prepare:
            prepare(args.prepare, args.output, args.suite)
            print(f"Prepared {args.prepare} at {args.output}; behavior: NOT RUN")
        else:
            suite = load_suite(args.suite)
            print(f"Validated {len(suite['cases'])} evaluation inputs; behavior: NOT RUN")
    except (ValueError, OSError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
