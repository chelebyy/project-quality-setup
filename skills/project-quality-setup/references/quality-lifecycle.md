# Quality decisions and maintenance

## Project decision record

Reuse the project's existing quality/testing document. If none exists during an authorized setup, create one concise document following repository conventions, such as `docs/quality.md`. Do not create competing reports or store project-specific state inside this global skill. Assessment-only requests return proposed entries without writing them. If an existing CI/testing document partially covers these decisions, extend it with the missing sections; create a separate linked decision record only when repository conventions or a clear audience boundary justify it, without duplicating commands or evidence.

Record only information that changes future decisions:

- Assessed revision/date, project/platform boundaries, relevant runtime and hosting assumptions.
- Check/tool decisions: selected or existing, omitted/deferred with reason, command/config location, local/CI trigger, and advisory/failing/verified-required status.
- Repository visibility, owner identity/type, observed GitHub plan and its evidence source/date; distinguish API/settings verification, user-reported information and unknowns. Record relevant feature entitlements and usage/cost constraints separately; no credentials, private billing details or invented cost estimates.
- Risk-to-test mapping, measured baseline/run evidence, and open work with next action.
- Significant decisions and why they changed, keeping history brief instead of appending every run log.
- For security scanning, retain the [coverage evidence, baseline and finding/exception decisions](security-scanning.md) needed to distinguish new issues, known debt and incomplete analysis. Reuse an existing finding tracker instead of duplicating sensitive reports here.

Read this record at subsequent invocations, then verify it against source, configuration and current remote evidence. It is a decision aid, not proof that old checks still run or that earlier plan entitlements remain valid. Preserve unrelated documentation.

## Risk-to-test mapping

Identify critical flows from the actual product and existing requirements. Candidate risks include sign-in/session expiry, role boundaries, payment correctness, irreversible data deletion, migrations, privacy/consent, and core content/navigation. Include only applicable risks; do not invent a payment system for a static website.

Use a compact table:

| Risk / flow | Expected observable outcome | Scenario / test location | Execution environment and trigger | Evidence / gap |
| --- | --- | --- | --- | --- |
| Applicable product risk | Success or denied/error behavior that must hold | Real test identifier/path, or missing | Local, PR, manual/device, etc. | Verified revision/run, partial, unverified or uncovered |

Where relevant, include positive and negative cases: a permitted operation succeeds while a different role is denied; a failed request does not persist partial state; a stored preference survives removal of a query override. Tie claims to assertions and execution, not just test names.

Prioritize gaps by impact and likelihood, keeping scope proportional to the setup request. Implement feasible in-scope scenarios; explicitly retain gaps requiring unavailable environments, business decisions or separate work. Passing unit tests may only partially cover an end-to-end risk. A skipped native test remains unverified. Never equate a line-coverage percentage with complete risk coverage.

## Intermittent failures and retries

1. Preserve the original failure, revision, environment, seed/test data where available, and useful logs/traces. A later pass does not delete the first failure from the report.
2. Compare bounded reruns under equivalent conditions. Distinguish deterministic product defects from test races, service outages, resource pressure or data/order dependence. Do not label an unexplained failure flaky merely because retry passed.
3. Fix the demonstrated cause: isolation, deterministic data, readiness conditions, selectors or real application behavior as appropriate. Avoid arbitrary sleeps, increasing retries without evidence, weaker assertions and blanket `continue-on-error`.
4. Use temporary quarantine only when justified and within the user's/project's authorization to weaken that check. Routine setup permission is not blanket authorization to remove an existing required protection. If no suitable authorization exists, keep the failing protection and report the concrete proposed exception.
5. For any quarantine, record exact tests, evidence, impact/coverage gap, tracked repair item (an existing issue or local task), actual accountable owner or explicitly unassigned status, review/expiry date and re-entry criterion. Do not create external issues/messages without authorization. Scope exclusions narrowly and continue visible diagnostic execution where practical.
6. At maintenance, flag overdue/unowned quarantines and prioritize repair/restoration; never silently extend them. A recorded expiry does not enforce itself: verify an existing enforcement mechanism or clearly document that it is checked on the next invocation. Restoration requires relevant verification, including the previously failing scenario.

Report pass-after-retry separately from a clean first-attempt pass. Measure first-attempt failures versus comparable executions when data is available; otherwise state the sample is insufficient rather than inventing a flake rate.

## Maintenance mode

Choose maintenance when the user requests upkeep or invokes setup on an already configured project. Existing partial setup can need both reconciliation and targeted additions; no forced migration is implied.

- Read the decision record and compare current manifests/platforms, critical flows, test scenarios, workflows/triggers, tool support, visibility and entitlements.
- Inspect a bounded representative sample of recent runs. Compare durations for like events/jobs/runners and similar workloads, separating queue time from execution where available. Report sample window/count and uncertainty; slower runs alone do not justify removing coverage.
- Identify new uncovered flows, broken commands, duplicate or obsolete checks, unused artifacts, stale quarantines and runtime/dependency drift. A rarely triggered release check is not obsolete merely because it has few runs.
- Reassess security exceptions and full-scan debt; compare tool/rule/scope changes before calling missing findings fixed. A change-aware clean PR does not close findings outside its analyzed scope.
- Keep working checks. Add or repair demonstrated gaps and tune expensive checks using measurements. Verify callers, required-check rules, consumers and authorization before retiring a job or changing its trigger; avoid leaving required statuses permanently pending.
- Re-run affected validation and refresh the same decision record with verified changes and unresolved work. Do not reset baselines to conceal regressions or auto-accept visual/performance changes.

Maintenance runs when invoked. Do not imply continuous monitoring or create a scheduler, hook or recurring task unless requested. A pilot in another repository is a separately selected application of the skill, not an automatic consequence of editing it.
