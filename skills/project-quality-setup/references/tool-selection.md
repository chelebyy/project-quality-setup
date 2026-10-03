# Tool selection by project and risk

Read only the sections matching detected source, manifests and workflow gaps. This is a decision catalog, not an installation checklist. Existing equivalent tools take precedence unless there is a demonstrated gap. Check current official documentation, version support, licenses and plan availability before generating commands/configuration; names here do not imply pinned versions or available entitlements.

For relevant candidates, record tool, evidence of applicability, purpose, local/CI placement and enforcement. Give a reason for selected, already covered, not applicable or deferred. No need to enumerate every irrelevant tool.

## React, JavaScript and web

| Candidate | When and purpose | Suggested placement / limits |
| --- | --- | --- |
| React Doctor | React/Next.js and compatible React Native/Expo code: framework-specific diagnostics and code-health findings | Evaluate explicitly after confirming supported version/framework. Local baseline, then PR diagnostics; consider changed-code scanning when supported. Decide severity/score policy from actual findings, not an arbitrary perfect-score requirement. |
| ESLint or existing JS/TS linter | Source rules appropriate to the framework | Local and PR; reuse current configuration, avoid overlapping full rule sets. |
| TypeScript compiler | TypeScript or an existing checked-JS setup | Local and PR type checking; distinguish this from transpilation/build success. |
| Prettier or existing formatter | Repository formatting conventions already adopted or requested | Check mode locally/PR; avoid repository-wide reformatting during quality setup. |
| Jest / Vitest / node:test | Unit/component/business logic tests using the current framework | Fast local/PR checks; choose an existing runner, not all three. Coverage is supporting evidence, not a substitute for useful assertions. |
| Playwright | Actual browser UI with critical flows | Small PR smoke suite; broader supported browser matrix scheduled/manual as justified. |
| axe-core browser integration | Rendered web accessibility states | Alongside relevant browser tests; deliberately cover themes/dialogs/focus/hover where relevant. |
| Lighthouse CI | Representative web routes needing lab performance/quality budgets | Limited sampling, initially advisory if variability unknown; schedule/manual or bounded PR checks. |

### React Doctor operating policy

Keep React Doctor distinct from tests, accessibility scans, and comprehensive security review. Its diagnostics and health score do not prove user flows work. Read-only diagnostic use is the default for setup assessment; automated source fixes or architecture rewrites are a separate scope.

Inspect existing React Doctor workflow/configuration before using an installer that generates another workflow. Verify scan scope and its base revision, exit behavior and diagnostic severity at the selected version. Start with actionable findings and an explicit gate policy; an advisory score should not silently become a required check. Existing known debt may justify a documented changed-code policy rather than blanket suppression.

Distinguish static diagnostics from optional live-app performance tracing. A trace requires a running representative app and covers only exercised interactions; native runtime coverage must be verified separately. PR comments are optional external messages: use job summaries/artifacts by default unless commenting is authorized, and do not grant write permissions merely to display a score.

Official source: https://github.com/millionco/react-doctor

## Dependency maintenance and supply chain

| Candidate | When and purpose | Suggested placement / limits |
| --- | --- | --- |
| Dependabot version updates | Supported manifests and GitHub Actions: propose routine dependency/action updates | Scheduled configuration with correct roots/ecosystems, sensible grouping and PR limits; preserve an existing Renovate/other update service instead of duplicating it. |
| Dependabot alerts and security updates | Detect known vulnerable dependencies and propose fixes where supported | Verify settings, dependency graph, ecosystem coverage and permissions separately. Security updates are alert-driven; a version-update schedule alone does not prove they are enabled. |
| Dependency Review action | Review dependency changes introduced by a PR | PR check when supported/entitled; policy for vulnerability severity and licenses based on actual project needs. Not the same as scanning the whole installed tree. |
| npm/pnpm/yarn audit, pip-audit, NuGet auditing | Appropriate ecosystem vulnerability assessment | Local/PR or scheduled according to cost and policy; distinguish production and development dependencies and preserve actionable failures. Verify current toolchain behavior. |
| Gitleaks | Secret detection gap not already covered adequately | Local/PR and initial history assessment where needed; scan scope matters. Remediation can require credential rotation, not just deleting text. |
| CodeQL / Semgrep | Supported-language static security analysis | Select based on languages, build needs, rules, license and GitHub entitlements; PR/default branch or schedule. Do not automatically run overlapping products. |

Dependabot runs are maintenance activity, not proof that application tests ran. Dependency update PRs must exercise appropriate project checks. Do not auto-merge updates or install an auto-merge workflow without authorization. Private registry authentication must use appropriate secret facilities and must not expose credentials to untrusted PR jobs.

Official sources:
- https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates
- https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-security-updates
- https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-dependency-review-action

## Mobile, backend and native projects

| Candidate | When and purpose | Suggested placement / limits |
| --- | --- | --- |
| Expo Doctor | Expo project dependency/configuration compatibility | Local and suitable PR validation; not a native build or device test. Verify supported SDK/tool versions. |
| Maestro / Detox | Native user journeys with provisioned app/emulator/device | Reuse current framework; small smoke where practical, heavier scheduled/manual runs. Preserve deliberate existing manual gating. |
| Ruff | Python lint/format checks | Local/PR if adopted or suitable; respect current formatting/lint tools. |
| pytest + coverage | Python behavior/integration tests | Local/PR, separate fixture tests from live provider calls; coverage thresholds require meaningful baseline. |
| pip check | Installed Python dependency compatibility | After representative install; complements pip-audit rather than replacing vulnerability scanning. |
| dotnet restore/build/test + existing xUnit/NUnit/MSTest | .NET compilation, unit/integration behavior | Local/PR under supported SDK; locked restore where configured; preserve established test runner. |
| .NET analyzers / format verification | Existing compiler/style analysis policies | Local/PR; avoid broad style rewrites or forcing unsupported analyzer packages. |
| go vet / go test | Go static checks and behavior | Local/PR; use supported OS/runtime matrix only where needed. |
| Firestore rules tests / equivalent authorization fixtures | Project actually uses database security rules | Isolated emulator/test environment, positive and denied-access cases; never infer coverage from compilation alone. |

## Workflows, containers and delivery artifacts

| Candidate | When and purpose | Suggested placement / limits |
| --- | --- | --- |
| actionlint | GitHub Actions YAML/expression/workflow mistakes | Local/PR for workflow changes; does not prove hosted execution succeeds. |
| Docker Compose configuration validation | Existing Compose services | Local/PR syntax/interpolation validation with safe test configuration; no secret output. |
| Container build and smoke tests | Application ships as a container | Build/start/readiness and meaningful request; verify expected non-root behavior if applicable. |
| Trivy / existing container scanner | Container vulnerability gap | Built-image PR/default/scheduled scans as appropriate; avoid redundant tools and choose actionable severity policy. |
| Publish/package smoke | Desktop/CLI/app produces distributable artifacts | Supported OS/RID/package validation, install/start smoke where feasible; packaging success does not authorize signing/upload/release. |
| Restore/recovery integration tests | Backup/restore is an actual product or deployment responsibility | Isolated fixtures/services, usually scheduled/manual; do not test restore against production. |
| Aggregate quality gate | Several conditional jobs need one stable required status | Explicitly propagate failures and distinguish intentional skips; verify rule/check naming and event coverage. |

Preserve useful repository-specific scripts (such as context lint, schema/phase audits, or custom security gates) after inspecting what they validate. Do not transplant them into unrelated projects merely because another repository uses them. Deployment workflows, AI review bots, and release automation are separate choices rather than automatic quality-setup additions.
