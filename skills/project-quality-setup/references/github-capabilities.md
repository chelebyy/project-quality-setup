# GitHub capabilities, cost, and trust

Verify current official documentation at use time. Visibility alone is insufficient: ownership, subscription, enabled products, policy, permissions, runner type and contribution source matter.

## Discover before choosing

1. Confirm exact repository, public/private/internal visibility, fork/upstream relationship and personal/organization ownership.
2. Inspect accessible Actions settings, runs, branch protection/rulesets, required checks and security settings. Never print secrets. API denial or inaccessible billing means unknown, not disabled or free.
3. Identify runner OS/architecture, standard/larger hosted runners, self-hosted trust boundaries, included usage and artifact/cache retention. Self-hosted does not mean costless or safe.
4. Determine which changes are supported and authorized. Continue independent work while reporting precise entitlement/permission gaps; ask narrowly only when a pending decision depends on them.

| Area | Decision rule |
| --- | --- |
| Actions usage | Public standard hosted runners and private included usage have different billing rules. Verify plan and runner class; larger runners can be billed even for public projects. Do not hardcode quota numbers. |
| Security products | Verify availability per feature, ownership, visibility and license. Do not assume a paid account includes all security products. |
| Merge enforcement | Check rule availability and authority to edit. A failed workflow does not itself block merging. Report workflow validation separately from verified enforcement. |
| Fork PRs | Use an unprivileged validation path. Secrets/write tokens may be unavailable; isolate privileged work instead of exposing them to untrusted code. |
| Permissions | Grant minimum job permissions. Do not execute untrusted PR code in privileged `pull_request_target`, secret-bearing jobs or trusted persistent self-hosted runners. |
| Artifacts | Retain only useful diagnostics with bounded retention, preferably on failure. Scrub sensitive traces/screenshots/responses. Do not send private diagnostics to public report hosting by default. |
| Spend/settings | Do not change visibility, buy plans, enable billed services, provision runners or raise billing limits to fit a template without authorization. |

## Efficient and reliable triggers

- Cancel superseded PR runs with appropriate concurrency, not release jobs indiscriminately.
- Cache using real lockfile/runtime inputs; prevent untrusted work from poisoning privileged execution.
- Limit matrices and performance sampling to supported targets and representative routes.
- Path-filtered required checks may never start and remain pending. Where useful, use an always-started aggregate gate that explicitly handles expected skips and upstream failures; verify real event behavior.
- Separate validation from deployment/publishing permissions and environments.
- A skipped E2E job is not executed coverage. Document manual flags, device and environment prerequisites.

## Official starting points

- Actions billing: https://docs.github.com/en/billing/concepts/product-billing/github-actions
- Security availability: https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security
- Rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets
- Actions security: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions

Follow redirects and verify current pages. If access fails, disclose the gap and avoid unsupported entitlement/price claims.
