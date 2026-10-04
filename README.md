# Skills by chelebyy

A collection of agent skills for practical software development. Each skill lives in its own directory and can be installed independently.

## Available skills

| Skill | Purpose |
| --- | --- |
| [project-quality-setup](skills/project-quality-setup/SKILL.md) | Choose and maintain a project's testing, security checks, GitHub CI, and branch/PR policies. Start with an idea or project documents, improve an existing repository, or reconcile a mature pipeline. |

`project-quality-setup` selects checks for the actual project instead of installing the same web stack everywhere.

## Install

```sh
npx skills add chelebyy/skills --skill project-quality-setup
```

For Codex only:

```sh
npx skills add chelebyy/skills --skill project-quality-setup --agent codex
```

The CLI lets you select supported agents and installation scope. See [skills CLI documentation](https://skills.sh/docs/cli). No model API subscription is required by this skill itself; your coding agent and selected tools have their own requirements.

## Use

In Codex, invoke `$project-quality-setup` with a concrete request, for example:

```text
$project-quality-setup Audit this repository's quality pipeline. Report gaps without changing files or GitHub settings.
```

```text
$project-quality-setup Set up appropriate local and PR checks for this project. Reuse existing tools and verify the result.
```

```text
$project-quality-setup Use these project documents to design a GitHub repository and staged CI plan before we write code. Do not create the remote repository yet.
```

```text
$project-quality-setup Review our existing checks, uncovered critical flows, flaky tests and CI duration. Implement relevant maintenance within the agreed scope.
```

Other agents may expose a different skill invocation UI. Instructions are in [SKILL.md](skills/project-quality-setup/SKILL.md) and respond in the user's language.

## What it covers

- Platform-aware selection: web, React, native/Expo, Python, .NET, Go, containers, libraries and documentation.
- Conditional tools such as React Doctor, Playwright, axe-core, Lighthouse CI, Expo Doctor, Dependabot, actionlint and relevant security scanners.
- Semgrep selection and gate policy, scan completeness evidence, existing security debt, and accountable finding/exception handling.
- Optional runtime security and infrastructure-as-code checks, such as ZAP or Checkov, only for applicable projects and authorized environments.
- Public/private visibility, GitHub entitlements, permissions, runner cost and untrusted contribution boundaries.
- PR requirements, real required checks, solo/team review policies, branch deletion/force-push protection and bypass visibility.
- Project decision records, risk-to-test mapping, intermittent-test handling and maintenance on later invocations.
- Read-only assessment of whether an existing deployment path waits for the intended CI checks for the deployed revision.

## Boundaries

This is an instruction skill, not a hosted service or autonomous background monitor. It does not promise full security, accessibility or test coverage. Tool versions, platform support and GitHub plan capabilities must be checked when used.

Assessment-only requests remain read-only. Repository creation/settings changes follow the user's actual authorization. The skill does not implicitly deploy, buy services, upload private documents, enable auto-merge or create scheduled tasks. CD setup is outside its default scope.

Use GitHub CLI for repository evidence when available and Context7 for current tool documentation when available, with official documentation as fallback. Neither integration is bundled, and credentials are never included.

## Structure and validation

Distributable skills live under `skills/<skill-name>/`, each with its own `SKILL.md`, agent metadata, and optional supporting files. Add each new skill to the table above. Supporting references for `project-quality-setup` are loaded by topic.

For repository development, use Python 3.12 or newer (CI uses 3.12), preferably in a virtual environment. The pinned YAML/Markdown parsers are development dependencies for these checks; skill installation and use do not require Python or these packages. Run:

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/eval_cases.py
python -m unittest discover -s tests
```

Validation discovers every skill directory and checks safe YAML parsing, nonempty name/description, duplicate keys, collection-required agent UI fields, and README catalog entries. This collection requires `interface.display_name`, a 25–64-character `short_description`, and a `default_prompt` mentioning the exact skill; these are collection conventions, not a complete external host schema. Optional policy/dependency metadata is preserved.

Local Markdown validation covers inline/reference links and images in README, skill documents and the evaluation guide; it ignores fenced/inline code examples and external URLs. It checks repository boundaries, file existence, and Markdown heading/custom-anchor targets, including duplicate headings. It does not fetch external pages, validate anchors in non-Markdown files, or emulate every GitHub rendering extension/raw HTML link. Every skill must have a real README link to its entrypoint.

The [behavioral evaluation inputs](evals/README.md) provide ten isolated scenarios and a preparation helper. Ordinary CI validates fixtures and preparation safety; it does **not** run a model or establish behavioral success. Keep actual agent transcripts, observed file changes and reviewer grading separate from packaging test results.

Contributions should include a realistic scenario and evidence for the proposed guidance, avoid universal rules derived from one project, and preserve authorization boundaries. Open a pull request with the scope and validation performed.

The [skills.sh directory](https://skills.sh) discovers skills through CLI installation telemetry; publication of this repository does not guarantee immediate listing or ranking. See its [FAQ](https://skills.sh/docs/faq).

## License

[MIT](LICENSE), copyright 2026 chelebyy. Mentioned projects and tools retain their own licenses and are not affiliated with this skill.
