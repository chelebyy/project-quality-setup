# Select a project profile

These are candidates, not mandatory bundles. Detect mixed projects/monorepos from source and manifests; configure affected roots without duplicating shared checks.

| Project | Useful baseline | Conditional additions |
| --- | --- | --- |
| Static website | Existing content/link/unit checks, preview, critical browser smoke | Playwright plus axe-core for real pages/states; limited Lighthouse CI on representative routes |
| Web application | Lint/types, unit tests, production build, relevant API/integration tests | Critical journeys in Playwright, rendered-state axe scans, stable visual regression baselines |
| API/backend | Compile/types, unit/service integration, migration/config validation | Contract tests, container smoke, authentication/authorization negative cases; browser tools only for actual UI |
| Expo/native mobile | Existing lint/types/unit tests, platform build validation | Existing Maestro/Detox or suitable native framework; explicitly provisioned emulator/device tests; web success does not prove native behavior |
| Desktop/.NET/CLI | Supported SDK restore/build, unit/integration, package smoke | Supported OS/RID matrix, signing/release validation separately scoped |
| Python/data/scraper | Existing lint/types where adopted, tests, dependency/install checks | Fixture-based parsers, container/service integration; bound and separate live-provider calls |
| Library | Supported-runtime build/test, API/package validation | Compatibility matrix and publish dry-run; no automatic publication |
| Documentation/config | Relevant syntax, link, schema or workflow lint | Documentation build/render if applicable |
| Empty/new | Use pre-code planning from the entrypoint; clarify purpose and document-backed decisions | Stage real checks as code appears; no placeholder application gates |
| Archived/fork | Determine active purpose and upstream relationship | Avoid a full application pipeline without an active application need |

## Web checks

- Playwright covers user behavior. Start with critical flows, semantic locators, isolated sessions, navigation/errors and state persistence. Cover relevant responsive and theme variations.
- axe-core detects a subset of accessibility issues. Exercise meaningful page states and dialogs. Hover/focus styles need deliberate checks; default-state scans do not cover all interactions. Never claim full accessibility compliance from automated results.
- Lighthouse CI provides sampled lab measurements. Use representative routes, stable builds and bounded sampling. Begin with advisory budgets where variability is unknown; derive enforceable thresholds from measured baselines. It does not replace functional tests, field performance or accessibility review.
- Test the actual serving mode. A static preview may not execute edge handlers, hosting redirects or production headers. Test an appropriate environment or report the gap.

## Security checks

Dependency advisories, secret detection, language-specific static analysis, container scanning, and authorization tests cover different risks. Review existing tools before adding another; select severity/enforcement explicitly and triage findings rather than suppressing categories.

Use native GitHub features only with verified availability. Ecosystem audits, Gitleaks, or suitable Semgrep rules can cover specific gaps but are not equivalent replacements for every CodeQL, secret-protection or supply-chain feature. Respect project exclusions and licenses. Keep sensitive data out of logs and report uploads.
