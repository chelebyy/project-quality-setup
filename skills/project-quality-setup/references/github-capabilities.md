# GitHub capabilities, cost, and trust

Verify current official documentation at use time. Visibility alone is insufficient: ownership, subscription, enabled products, policy, permissions, runner type and contribution source matter.

## Discover before choosing

1. Confirm exact repository, public/private/internal visibility, fork/upstream relationship and personal/organization ownership.
2. Check the repository owner's GitHub subscription explicitly: Free/Pro for a personal account, or Free/Team/Enterprise for an organization as applicable. Keep repository visibility, owner plan, feature entitlements and the current caller's permissions as separate facts.
3. Inspect accessible Actions settings, runs, branch protection/rulesets, required checks and security settings. Never print secrets. API denial or inaccessible billing means unknown, not disabled or free.
4. Identify runner OS/architecture, standard/larger hosted runners, self-hosted trust boundaries, included usage and artifact/cache retention. Self-hosted does not mean costless or safe.
5. Determine which changes are supported and authorized. Continue independent work while reporting precise entitlement/permission gaps; ask narrowly only when a pending decision depends on them.

### Plan evidence

- Use the verified repository owner and GitHub host. For a personally owned repository, a read-only authenticated-user lookup (`GET /user`) can provide `plan.name` when available; use it only if the authenticated login matches that owner. A collaborator's Pro plan does not establish the owner's plan.
- For an organization-owned repository, inspect accessible organization plan information (`GET /orgs/{org}`) or the organization's authorized billing/settings view. The authenticated person's subscription is not the organization's plan. Enterprise-managed organizations may require owner/enterprise billing evidence. Check current endpoint and permission documentation; a successful public profile lookup need not expose plan information.
- Keep only the owner identity/type, visibility, observed plan label, evidence source/date and the feature decisions it supports. Filter API output to these fields before reporting or retaining it; do not dump profiles, billing contacts, payment details or credentials. Do not automatically request broader token scopes or enable a paid plan to complete discovery.
- Report a missing, null, denied or ambiguous plan as unknown, with the missing evidence. Do not infer Free from absent data, Pro from private visibility, or a current product tier from an unfamiliar/legacy API label. An explicit user-provided plan can inform the decision, labeled as user-reported rather than independently verified. Ask only for the owner plan when that unknown changes a pending choice; continue independent checks meanwhile.
- Verify selected feature availability and accessible usage/budget information separately from the plan name using current official documentation. Copilot subscriptions and separately licensed security products are not proof of the repository owner's core GitHub plan. A plan's included allowance is not evidence of remaining quota or zero cost. If cost cannot be established, prepare bounded CI configuration and report the gap before any execution requiring additional spend authorization.

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

- GitHub plans: https://docs.github.com/en/get-started/learning-about-github/githubs-plans
- Authenticated user: https://docs.github.com/en/rest/users/users#get-the-authenticated-user
- Organization plan access: https://docs.github.com/en/rest/orgs/orgs#get-an-organization
- Actions billing: https://docs.github.com/en/billing/concepts/product-billing/github-actions
- Security availability: https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security
- Rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets
- Actions security: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions

Follow redirects and verify current pages. If access fails, disclose the gap and avoid unsupported entitlement/price claims.
