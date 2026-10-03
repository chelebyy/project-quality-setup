# Project Quality Setup

An agent skill for choosing and maintaining a project's testing, security checks, GitHub CI, and branch/PR policies. Start with an idea or project documents, improve an existing repository, or reconcile a mature pipeline.

It selects checks for the actual project instead of installing the same web stack everywhere.

## Install

```sh
npx skills add chelebyy/project-quality-setup --skill project-quality-setup
```

For Codex only:

```sh
npx skills add chelebyy/project-quality-setup --skill project-quality-setup --agent codex
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
- Public/private visibility, GitHub entitlements, permissions, runner cost and untrusted contribution boundaries.
- PR requirements, real required checks, solo/team review policies, branch deletion/force-push protection and bypass visibility.
- Project decision records, risk-to-test mapping, intermittent-test handling and maintenance on later invocations.
- Read-only assessment of whether an existing deployment path waits for the intended CI checks for the deployed revision.

## Boundaries

This is an instruction skill, not a hosted service or autonomous background monitor. It does not promise full security, accessibility or test coverage. Tool versions, platform support and GitHub plan capabilities must be checked when used.

Assessment-only requests remain read-only. Repository creation/settings changes follow the user's actual authorization. The skill does not implicitly deploy, buy services, upload private documents, enable auto-merge or create scheduled tasks. CD setup is outside its default scope.

Use GitHub CLI for repository evidence when available and Context7 for current tool documentation when available, with official documentation as fallback. Neither integration is bundled, and credentials are never included.

## Structure and validation

The distributable skill lives under `skills/project-quality-setup/`. Supporting references are loaded by topic. Run the dependency-free repository check with:

```sh
python scripts/validate.py
```

This checks packaging, required metadata and relative Markdown links; it does not prove behavioral quality on every project. Contributions should include a realistic scenario and evidence for the proposed guidance, avoid universal rules derived from one project, and preserve authorization boundaries. Open a pull request with the scope and validation performed.

The [skills.sh directory](https://skills.sh) discovers skills through CLI installation telemetry; publication of this repository does not guarantee immediate listing or ranking. See its [FAQ](https://skills.sh/docs/faq).

## License

[MIT](LICENSE), copyright 2026 chelebyy. Mentioned projects and tools retain their own licenses and are not affiliated with this skill.
