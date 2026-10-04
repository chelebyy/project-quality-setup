# Security scans, evidence and findings

Read the relevant sections when selecting a source scanner, configuring its gate, or handling its findings. Reuse the project's existing security workflow and decision record; another scanner is useful only for a demonstrated coverage gap.

## Semgrep operating policy

1. Establish applicable languages/frameworks, security risks and existing CodeQL/Semgrep/equivalent coverage. Check language and rule support for the chosen engine/version. Community Edition and platform/advanced analysis are not interchangeable; do not promise cross-file coverage from a scan that lacks it.
2. Choose account-free local scanning or an authorized platform integration deliberately. `semgrep scan` can use selected local or registry rules without an account. A local process is not necessarily offline: rule downloads, metrics, findings and integrations have distinct data flows. Verify current settings, licenses, authentication, cost and upload behavior before using private source or enabling platform features. Preserve existing authorized integrations; do not create accounts or transmit diagnostics just to obtain a dashboard.
3. Start with relevant rules and an observed baseline. Record the rule/configuration identity and tool version so a rule update can be distinguished from a new code defect. Avoid an unreviewed all-rules bundle, blanket severity suppression, arbitrary perfect-score gates, or adding overlapping scanners without a reason.
4. Select full versus change-aware scanning using the policy below. Verify the actual checkout, comparison revision, rule set and exit behavior; the command name or a green job is insufficient evidence.
5. Test project-specific rules with small matching and non-matching fixtures, including a corrected example. Use Semgrep's supported rule-test command at the selected version. Rule fixtures are source to analyze, not programs to execute. A rule test validates that rule's examples, not the absence of vulnerabilities in the application.

### Findings and execution errors are separate gates

Verify these semantics against the installed version before generating commands:

| Mode | Gate implication |
| --- | --- |
| `semgrep scan` | By default, a completed scan can exit successfully even with findings. If findings should fail the job, configure the documented behavior such as `--error` for the selected rules. |
| Platform-backed `semgrep ci` | Blocking policy determines which findings fail the job; findings marked advisory remain visible. Do not assume every severity is blocking. |
| `semgrep ci` execution errors | Documented default suppression can make internal errors pass. For a required scan, use supported error propagation such as `--no-suppress-errors` and verify the resulting job behavior. |

Do not infer completeness from exit codes alone. Per-file parse errors, timeouts or skipped targets may leave partial coverage even when the overall process finishes. Apply the scan evidence contract below. A deliberately advisory scan may remain nonblocking, but its failed/incomplete state must remain visible and must not be reported as a clean scan. Avoid `|| true` or unconditional success wrappers that erase the distinction.

## Scan evidence contract

For each selected scanner, record the intended scope and inspect its supported summary/structured output:

- Assessed revision, scanner version, engine/mode and rule/configuration identity.
- Expected source roots/languages and actual targets/rules analyzed; exclusions, generated/vendor files and relevant size limits.
- Completion state, parse/configuration/authentication failures, timeouts and skipped relevant files. Use version-specific fields instead of inventing a common JSON schema for unrelated tools.
- Findings and their gate disposition, separately from execution failures and missing coverage.

Use **complete**, **partial**, **failed**, **not applicable** or **unknown** with evidence. Zero findings is not proof that targets were analyzed. A documentation-only PR can legitimately have no applicable source changes; record that specific reason. If applicable source exists but no relevant targets/rules ran, do not call it clean. A required check must not signal accepted protection when its required coverage is missing; fail it or use an explicitly authorized, visible exception. Do not make unrelated/unsupported languages an automatic failure if they are outside the selected scope.

For new gates, use isolated fixtures or a supported local simulation to show that a representative finding and an execution failure cannot silently become success. Never push a failing probe or execute a harmful payload against a real system to demonstrate this. Report unexercised error paths honestly.

## Existing debt and new findings

Establish an initial full baseline where feasible and keep its known findings visible. Change-aware PR scanning can focus a gate on new problems while existing debt has accountable repair work; it is not permission to hide all pre-existing findings. Confirm the real target/comparison revision and tool-specific baseline semantics, especially in shallow checkouts and integration branches.

Complement change-aware checks with an appropriate full scan when justified and authorized, for example on the default branch or an agreed manual/scheduled workflow. Changes to rules, shared configuration or dependency analysis may need a full scan even when a source diff is small. Existing urgent findings still need triage; being old does not make a finding acceptable. Do not reset a baseline merely to make a PR pass.

## Finding and exception lifecycle

Verify a reported issue against the relevant source and context before classifying it. Severity is one input; reachability, exposure, affected data and existing mitigations affect priority. Use conclusive static evidence where sufficient, and safe runtime verification only when needed and authorized.

| Disposition | Required basis and next step |
| --- | --- |
| Needs investigation | Evidence is insufficient; record the missing fact and next action. Do not silently call it a false positive. |
| Confirmed | Source or safe execution supports the issue; repair within scope and verify the affected behavior. |
| False positive | Record why this rule does not apply to this occurrence. Prefer a narrow rule/location-specific exception with reviewable evidence. |
| Accepted risk | An authorized decision accepts the identified residual risk, with a real owner and review date. The agent cannot invent acceptance to clear CI. |
| Deferred repair | Preserve the finding, rationale, accountable owner or explicitly unassigned status, next action and review/expiry date. Deferral does not automatically waive a required gate. |

Reuse the current tracker or quality record. Store a stable rule/finding identifier, location/revision, disposition, evidence, exception scope and gate effect; avoid copying secrets or unnecessary vulnerable source into reports. Creating external tickets/comments remains subject to actual authorization. Suppressing a finding or weakening a required gate requires the appropriate existing authorization, not just a scanner recommendation.

Verify a fix with the relevant scan and behavior regression check. On maintenance, revisit expired/unowned exceptions and restore protection where appropriate; a written expiry is not automatic enforcement. Do not extend an exception or close a finding merely because a newer report omitted it: changed scope/rules or scan failure may explain the absence.

## Official references

Check current documentation at use time; hosted policy and CLI behavior can evolve.

- [Semgrep CLI reference](https://semgrep.dev/docs/cli-reference)
- [Blocking findings and errors in CI](https://semgrep.dev/docs/semgrep-ci/configuring-blocking-and-errors-in-ci)
- [Community Edition customization and rule tests](https://semgrep.dev/docs/customize-semgrep-ce)
- [CLI versus CI scan differences](https://semgrep.dev/docs/kb/semgrep-ci/ci-vs-cli)
- [Semgrep data collection](https://github.com/semgrep/semgrep/blob/develop/metrics.md)
