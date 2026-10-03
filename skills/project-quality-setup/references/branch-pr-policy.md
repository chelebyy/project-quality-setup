# Branch and PR policy

Assess effective rules, not just a proposed configuration. Identify the actual default branch and any explicitly selected integration branches; do not assume the name is main. Inspect existing branch protections and applicable repository/organization rulesets, enforcement state, targets and exceptions. Check current GitHub plan/ownership support using the capabilities reference.

## Policy choices

| Control | Selection guidance |
| --- | --- |
| PR before merge | Prefer a reviewable PR path for the default branch; inspect direct-push and bypass permissions. Fit initial repository bootstrap and existing integrations without blanket exceptions. |
| Required status checks | Select stable, observed check names and intended source app where supported. Require relevant tests/build/security checks, not every advisory metric. Ensure event/path coverage and failure propagation. |
| Human approvals | Solo projects can use PRs and required CI without requiring an unavailable second person. Teams should choose an achievable review count based on risk and reviewer availability. Never invent reviewers. |
| Stale/latest-push approval | Evaluate how new commits affect prior approvals. Require fresh or independent latest-push approval when suitable; verify that real eligible reviewers exist. |
| CODEOWNERS | Add only with real responsible users/teams and valid access. Optional in solo projects; do not create fictional ownership or mandate inaccessible team approval. |
| Conversation resolution | Consider requiring review conversations to be resolved. Resolution state is not proof a finding was fixed; preserve evidence-led review and never auto-resolve feedback merely to unlock merge. |
| Force-push and branch deletion | Prefer preventing these on protected integration/default branches; preserve existing intentional exceptions only after understanding them. Do not test enforcement by attempting destructive operations. |
| Admin/bot bypass | List effective actors, capabilities and scope. Avoid broad exemptions; maintenance bots do not automatically need bypass rights. Record intentional emergency access and its limitations. |
| Up-to-date branch / merge queue | Evaluate integration risk, CI cost and existing workflow support. Do not mandate for every solo repo; if a queue is selected, verify its validation events and required checks. |
| Merge methods / history | Respect existing conventions. Signed commits, linear history and squash-only policies are conditional choices, not universal requirements. |

## Safe activation

1. Report current versus proposed effective policy, supported/unavailable controls and solo/team assumptions. Unavailable paid features remain explicit gaps; do not change visibility or purchase plans to enable them.
2. Confirm implementation of repository settings is within the user's actual request. Continue already authorized changes without redundant confirmation; do not treat an audit or skill edit as permission to alter remote repositories.
3. Before a settings change, capture the relevant existing configuration without secrets and prepare a bounded correction/restoration path. Preserve unrelated and inherited rules; do not disable organization controls to force a local template.
4. Establish real workflows/check identities before requiring their statuses. For an empty repository, stage bootstrap explicitly rather than requiring non-existent tests or granting permanent broad bypass. Never create an always-green placeholder to represent future coverage.
5. Apply only supported, in-scope changes. Re-read effective configuration and evaluate available real PR/check evidence, including bypass paths. A successful API update alone does not prove an ordinary contributor is gated.

Distinguish configuration verified, actual enforcement observed, untested behavior and blocked/unknown. Required-check acceptance can differ from actual test execution: inspect skipped/neutral/conditional jobs and aggregate logic against current GitHub semantics. A branch gate is not proof that an external deployment waits for CI; route that question to the separate read-only CI-to-release assessment.

## Official sources

Verify current documentation before generating settings/API payloads; GitHub.com and Enterprise Server support may differ.

- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
